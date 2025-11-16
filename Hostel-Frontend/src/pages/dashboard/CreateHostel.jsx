import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../../utils/api";

const CreateHostel = () => {
  const [formData, setFormData] = useState({
    name: "",
    university: "",
    rooms: "",
    price: "",
    description: "",
    images: [],
    amenities: {
      wifi: false,
      water: false,
      electricity: false,
      furnished: false,
      transport_to_campus: false
    }
  });
  const [error, setError] = useState("");

  const universities = [
    "University of Nairobi",
    "Kenyatta University",
    "Jomo Kenyatta University of Agriculture and Technology",
    "Strathmore University",
    "United States International University Africa",
    "Catholic University of Eastern Africa",
    "KCA University",
    "Mount Kenya University",
    "Technical University of Kenya",
    "Kenyatta International Conference Centre"
  ];

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setFormData({
        ...formData,
        amenities: {
          ...formData.amenities,
          [name]: checked
        }
      });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    const imageUrls = files.map(file => URL.createObjectURL(file));
    setFormData({ ...formData, images: imageUrls });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const token = localStorage.getItem("token");

      const payload = {
        name: formData.name,
        location: formData.university,
        price: parseFloat(formData.price),
        capacity: parseInt(formData.rooms, 10) || 1,
        room_type: 'shared', // default room_type
        description: formData.description,
        images: formData.images,
        amenities: formData.amenities
      };

      await axios.post(`${API_BASE_URL}/hostels/`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      navigate("/dashboard/my-hostels"); // corrected route
    } catch (err) {
      console.error("Failed to create hostel:", err);
      setError(err.response?.data?.message || "Failed to create hostel");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Create New Hostel</h1>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-md">
        <input
          name="name"
          placeholder="Hostel Name"
          value={formData.name}
          onChange={handleChange}
          required
          className="border p-2 rounded"
        />
        <select
          name="university"
          value={formData.university}
          onChange={handleChange}
          required
          className="border p-2 rounded"
        >
          <option value="">Select University</option>
          {universities.map((university) => (
            <option key={university} value={university}>
              {university}
            </option>
          ))}
        </select>
        <input
          name="rooms"
          type="number"
          min="1"
          placeholder="Number of Rooms"
          value={formData.rooms}
          onChange={handleChange}
          required
          className="border p-2 rounded"
        />
        <input
          name="price"
          type="number"
          min="0"
          step="0.01"
          placeholder="Price per month"
          value={formData.price}
          onChange={handleChange}
          required
          className="border p-2 rounded"
        />

        {/* Amenities Checkboxes */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Amenities:</label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="checkbox"
                name="wifi"
                checked={formData.amenities.wifi}
                onChange={handleChange}
                className="mr-2"
              />
              WiFi Available
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="water"
                checked={formData.amenities.water}
                onChange={handleChange}
                className="mr-2"
              />
              Water Available
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="electricity"
                checked={formData.amenities.electricity}
                onChange={handleChange}
                className="mr-2"
              />
              Electricity Available
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="furnished"
                checked={formData.amenities.furnished}
                onChange={handleChange}
                className="mr-2"
              />
              Furnished
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="transport_to_campus"
                checked={formData.amenities.transport_to_campus}
                onChange={handleChange}
                className="mr-2"
              />
              Transport to Campus
            </label>
          </div>
        </div>

        <textarea
          name="description"
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
          className="border p-2 rounded"
        />

        {/* Image Upload */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Hostel Images:</label>
          <input
            type="file"
            multiple
            accept="image/*"
            onChange={handleImageChange}
            className="border p-2 rounded w-full"
          />
          {formData.images.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {formData.images.map((image, index) => (
                <img
                  key={index}
                  src={image}
                  alt={`Hostel image ${index + 1}`}
                  className="w-20 h-20 object-cover rounded border"
                />
              ))}
            </div>
          )}
        </div>

        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Create Hostel
        </button>
      </form>
    </div>
  );
};

export default CreateHostel;
