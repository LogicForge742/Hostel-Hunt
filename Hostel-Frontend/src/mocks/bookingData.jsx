export const mockHostels = [
  {
    id: 1,
    name: "Sunset Backpackers",
    location: "Barcelona, Spain",
    price: 25,
    rating: 4.5,
    image: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400",
    amenities: ["WiFi", "Kitchen", "Bar", "Lockers"],
    description: "A vibrant hostel in the heart of Barcelona with rooftop views."
  },
  {
    id: 2,
    name: "Mountain View Lodge",
    location: "Bern, Switzerland",
    price: 35,
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400",
    amenities: ["WiFi", "Breakfast", "Laundry", "Mountain Views"],
    description: "Cozy hostel with stunning alpine views and modern facilities."
  },
  {
    id: 3,
    name: "City Central Hostel",
    location: "Amsterdam, Netherlands",
    price: 28,
    rating: 4.3,
    image: "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400",
    amenities: ["WiFi", "Bike Rental", "Bar", "Tours"],
    description: "Perfect location for exploring Amsterdam's canals and culture."
  }
];

export const mockBookings = [
  {
    id: 1,
    hostelId: 1,
    userId: 1,
    checkIn: "2024-02-15",
    checkOut: "2024-02-18",
    guests: 2,
    totalPrice: 75,
    status: "confirmed",
    bookingDate: "2024-01-20"
  },
  {
    id: 2,
    hostelId: 2,
    userId: 1,
    checkIn: "2024-03-10",
    checkOut: "2024-03-15",
    guests: 1,
    totalPrice: 175,
    status: "upcoming",
    bookingDate: "2024-01-25"
  },
  {
    id: 3,
    hostelId: 3,
    userId: 1,
    checkIn: "2024-01-05",
    checkOut: "2024-01-08",
    guests: 3,
    totalPrice: 84,
    status: "completed",
    bookingDate: "2023-12-15"
  }
];

export const mockUser = {
  id: 1,
  name: "John Doe",
  email: "john@example.com",
  favorites: [1, 3]
};
