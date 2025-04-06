// How to quickly recompile
// ========================
// - Start by installing normally, but without deleting all the intermediate 
//   files.  This step will be as slow as a normal install:
//
//     $ pip install --no-clean .
//
// - After one `pip install` fails, you can copy the compiler command from the 
//   error message.  This doesn't actually update the python installation, 
//   though, so after compilation succeeds, you need to run `pip install`.

#include <Eigen/Dense>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include <string>
#include <cstdint>
#include <algorithm>
#include <vector>
#include <iostream>

#define watch(x) std::cerr << (#x) << ": " << (x) << std::endl
#define watchv(x) std::cerr << (#x) << std::endl << (x) << std::endl << std::endl

namespace py = pybind11;

using Eigen::Vector3d;
using Eigen::Vector4d;
using Eigen::Matrix3d;
using Eigen::Matrix4d;

long
_find_visible_residues(
		py::array_t<int64_t> residue_ids,
		py::array_t<int64_t> backbone_ids,
		py::array_t<double> atom_x_A,
		py::array_t<double> atom_y_A,
		py::array_t<double> atom_z_A,
		py::array_t<double> atom_occupancies,

		Vector3d probe_center_A,
		Vector3d boundary_min_corner_A,
		Vector3d boundary_max_corner_A,

		py::array_t<int64_t> out_indices,
		py::array_t<double> out_coords_A) {

	auto residue_id_getter = residue_ids.template unchecked<1>();
	auto backbone_id_getter = backbone_ids.template unchecked<1>();
	auto x_getter = atom_x_A.template unchecked<1>();
	auto y_getter = atom_y_A.template unchecked<1>();
	auto z_getter = atom_z_A.template unchecked<1>();
	auto occupancy_getter = atom_occupancies.template unchecked<1>();

	auto n_backbone = residue_id_getter.size();
	auto n_pick = out_indices.size();

	if ((n_backbone < 3) || (n_pick < 1)) {
		return 0;
	}

	long i = 0;
	long o = -1;
	bool is_last_residue = false;
	long last_residue_id = -1;

	Vector4d probe_in_residue_frame(
			probe_center_A[0],
			probe_center_A[1],
			probe_center_A[2],
			1);

	long max_residue_id = residue_ids.at(n_backbone - 1);
	std::vector<double> best_occupancies(max_residue_id + 1, 0);

	while (i + 3 <= n_backbone) {
		long residue_id = residue_id_getter(i);

		// Stop if we've already processed the last residue.
		if (is_last_residue && residue_id != last_residue_id) {
			break;
		}

		long j = i + 1;
		long k = i + 2;

		// Check that all atoms belong to the same residue.
		if (residue_id != residue_id_getter(j)) {
			i = j;
			continue;
		}
		if (residue_id != residue_id_getter(k)) {
			i = k;
			continue;
		}

		// Check that the atoms are in the expected order.
		if (backbone_id_getter(i) != 0) {
			i = k + 1;
			continue;
		}
		if (backbone_id_getter(j) != 1) {
			i = k + 1;
			continue;
		}
		if (backbone_id_getter(k) != 2) {
			i = k + 1;
			continue;
		}

		// Check that this is the most occupied alternate conformation.
		double occupancy = std::min({
				occupancy_getter(i),
				occupancy_getter(j),
				occupancy_getter(k)
		});
		if (occupancy <= best_occupancies[residue_id]) {
			i = k + 1;
			continue;
		}

		Vector3d xyz_n(
				x_getter(i),
				y_getter(i),
				z_getter(i));
		Vector3d xyz_ca(
				x_getter(j),
				y_getter(j),
				z_getter(j));
		Vector3d xyz_c(
				x_getter(k),
				y_getter(k),
				z_getter(k));

		Vector3d e1 = xyz_n - xyz_ca;
		e1.normalize();

		Vector3d e2 = xyz_c - xyz_ca;
		e2 = e2 - e1 * e1.dot(e2);
		e2.normalize();

		Vector3d e3 = e1.cross(e2);

		Matrix3d R = Matrix3d::Zero();
		R.col(0) = e1;
		R.col(1) = e2;
		R.col(2) = e3;

		Matrix4d RT = Matrix4d::Identity();
		RT.topLeftCorner<3, 3>() = R;
		RT.col(3).head<3>() = xyz_ca;

		Vector3d probe = (RT * probe_in_residue_frame).head<3>();

		bool out_of_bounds = (
				(probe.array() < boundary_min_corner_A.array()).any() ||
				(probe.array() > boundary_max_corner_A.array()).any()
		);

		if (out_of_bounds) {
			i = k + 1;
			continue;
		}

		o += (residue_id != last_residue_id);
		last_residue_id = residue_id;
		is_last_residue = (o == n_pick - 1);

		out_indices.mutable_at(o) = i;
		out_coords_A.mutable_at(o, 0) = probe(0);
		out_coords_A.mutable_at(o, 1) = probe(1);
		out_coords_A.mutable_at(o, 2) = probe(2);

		i = k + 1;
	}

	return o + 1;
}

PYBIND11_MODULE(_inner_loop, m) {

	m.def(
			"_find_visible_residues",
			&_find_visible_residues,
			py::arg("residue_ids").noconvert(),
			py::arg("backbone_ids").noconvert(),
			py::arg("atom_x_A").noconvert(),
			py::arg("atom_y_A").noconvert(),
			py::arg("atom_z_A").noconvert(),
			py::arg("atom_occupancies").noconvert(),
			py::arg("probe_center_A"),
			py::arg("boundary_min_corner_A"),
			py::arg("boundary_max_corner_A"),
			py::arg("out_indices").noconvert(),
			py::arg("out_coords_A").noconvert());

}


