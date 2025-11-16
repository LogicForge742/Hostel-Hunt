import { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../utils/api";
import { useNavigate } from "react-router-dom";

const MyHostels = () => {
  const [hostels, setHostels] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchHostels();
  }, []);

  const fetchHostels = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(`${API_BASE_URL}/hostels/my-hostels`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Backend returns { hostels: [...], total, pages }
      setHostels(res.data.hostels || []);
    } catch (err) {
      console.error("Failed to fetch hostels:", err);
      setError("Failed to load hostels");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this hostel?")) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`${API_BASE_URL}/hostels/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHostels(hostels.filter(hostel => hostel.id !== id)); // Adjusted for backend id
    } catch (err) {
      console.error("Failed to delete hostel:", err);
      setError("Failed to delete hostel");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">My Hostels</h1>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <button
        className="mb-4 px-4 py-2 bg-blue-500 text-white rounded"
        onClick={() => navigate("/dashboard/hostels/create")} // Corrected path
      >
        + Create New Hostel
      </button>

      {hostels.length === 0 ? (
        <p>No hostels found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {hostels.map(hostel => (
            <div key={hostel.id} className="border p-4 rounded shadow"> {/* Adjusted key */}
              <h2 className="text-lg font-semibold">{hostel.name}</h2>
              <p>{hostel.location}</p>
              <div className="mt-2 flex gap-2">
                <button
                  className="px-2 py-1 bg-yellow-400 rounded"
                  onClick={() => navigate(`/dashboard/hostels/edit/${hostel.id}`)} // Corrected path
                >
                  Edit
                </button>
                <button
                  className="px-2 py-1 bg-red-500 text-white rounded"
                  onClick={() => handleDelete(hostel.id)} // Adjusted for id
                >
                  Delete
                </button>
                <button
                  className="px-2 py-1 bg-gray-200 rounded"
                  onClick={() => navigate(`/hostel/${hostel.id}`)} // View stays the same
                >
                  View
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyHostels;
