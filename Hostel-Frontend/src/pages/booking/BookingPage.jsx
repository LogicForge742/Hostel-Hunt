import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { useBooking } from '../../context/BookingContext.jsx';
import Button from '../../components/Button.jsx';

export default function BookingPage() {
  const { hostelId } = useParams();
  const navigate = useNavigate();
  const { getHostelById, createBooking } = useBooking();

  const [step, setStep] = useState(1);
  const [bookingData, setBookingData] = useState({
    checkIn: null,
    checkOut: null,
    guests: 1,
    phoneNumber: ''
  });

  const hostel = getHostelById(hostelId);

  if (!hostel) {
    return <div className="min-h-screen flex items-center justify-center">Hostel not found</div>;
  }

  const handleDateChange = (field, date) => {
    setBookingData(prev => ({ ...prev, [field]: date }));
  };

  const handleGuestsChange = (guests) => {
    setBookingData(prev => ({ ...prev, guests: parseInt(guests) }));
  };

  const calculateMonths = () => {
    if (!bookingData.checkIn || !bookingData.checkOut) return 0;
    const diffTime = Math.abs(bookingData.checkOut - bookingData.checkIn);
    const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(1, Math.round(days / 30)); // At least 1 month, round to nearest month
  };

  const calculateTotal = () => {
    const months = calculateMonths();
    const pricePerMonth = hostel.price;
    return months * pricePerMonth * bookingData.guests;
  };

  const handleNext = () => {
    if (step === 1) {
      if (!bookingData.checkIn || !bookingData.checkOut) {
        alert('Please select check-in and check-out dates');
        return;
      }
      // Validate that check-out is after check-in
      if (bookingData.checkIn >= bookingData.checkOut) {
        alert('Check-out date must be after check-in date');
        return;
      }
      // Validate that check-in is not in the past
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (bookingData.checkIn < today) {
        alert('Check-in date cannot be in the past');
        return;
      }
    }
    if (step === 2 && (bookingData.guests < 1 || !bookingData.phoneNumber)) {
      alert('Please select at least 1 guest and provide a phone number');
      return;
    }
    setStep(step + 1);
  };

  const handleConfirm = async () => {
    try {
      // Format dates as YYYY-MM-DD without timezone conversion
      const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
      };

      const bookingId = await createBooking({
        hostel_id: parseInt(hostelId),
        check_in: formatDate(bookingData.checkIn),
        check_out: formatDate(bookingData.checkOut),
        guests: bookingData.guests,
        phone_number: bookingData.phoneNumber
      });
      navigate(`/booking/confirmation/${bookingId}`);
    } catch (error) {
      alert('Failed to create booking: ' + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-4">Book {hostel.name}</h1>
            <div className="flex items-center space-x-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>1</div>
              <span className={step >= 1 ? 'text-blue-600' : 'text-gray-400'}>Select Dates</span>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>2</div>
              <span className={step >= 2 ? 'text-blue-600' : 'text-gray-400'}>Guests</span>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>3</div>
              <span className={step >= 3 ? 'text-blue-600' : 'text-gray-400'}>Confirm</span>
            </div>
          </div>

          {step === 1 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Select Dates</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Check-in Date</label>
                  <DatePicker
                    selected={bookingData.checkIn}
                    onChange={(date) => handleDateChange('checkIn', date)}
                    minDate={new Date()}
                    className="w-full p-3 border rounded-lg"
                    placeholderText="Select check-in date"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Check-out Date</label>
                  <DatePicker
                    selected={bookingData.checkOut}
                    onChange={(date) => handleDateChange('checkOut', date)}
                    minDate={bookingData.checkIn || new Date()}
                    className="w-full p-3 border rounded-lg"
                    placeholderText="Select check-out date"
                  />
                </div>
              </div>
              <Button
                onClick={handleNext}
                disabled={!bookingData.checkIn || !bookingData.checkOut}
                variant="primary"
              >
                Next
              </Button>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Booking Details</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Number of Guests</label>
                  <select
                    value={bookingData.guests}
                    onChange={(e) => handleGuestsChange(e.target.value)}
                    className="w-full p-3 border rounded-lg"
                  >
                    {[1, 2, 3, 4, 5, 6].map(num => (
                      <option key={num} value={num}>{num} Guest{num > 1 ? 's' : ''}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input
                    type="tel"
                    value={bookingData.phoneNumber}
                    onChange={(e) => setBookingData(prev => ({ ...prev, phoneNumber: e.target.value }))}
                    placeholder="Enter your phone number"
                    className="w-full p-3 border rounded-lg"
                    required
                  />
                </div>
              </div>
              <div className="flex space-x-4">
                <Button
                  onClick={() => setStep(1)}
                  variant="secondary"
                >
                  Back
                </Button>
                <Button
                  onClick={handleNext}
                  disabled={!bookingData.phoneNumber}
                  variant="primary"
                >
                  Next
                </Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Confirm Booking</h2>
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-xl font-semibold mb-4">{hostel.name}</h3>
                <div className="space-y-2">
                  <p><strong>Check-in:</strong> {bookingData.checkIn?.toLocaleDateString()}</p>
                  <p><strong>Check-out:</strong> {bookingData.checkOut?.toLocaleDateString()}</p>
                  <p><strong>Months:</strong> {calculateMonths()}</p>
                  <p><strong>Guests:</strong> {bookingData.guests}</p>
                  <p><strong>Phone Number:</strong> {bookingData.phoneNumber}</p>
                  <p><strong>Price per month:</strong> KSh {hostel.price}</p>
                  <p className="text-xl font-bold"><strong>Total:</strong> KSh {calculateTotal()}</p>
                </div>
              </div>
              <div className="flex space-x-4">
                <Button
                  onClick={() => setStep(2)}
                  variant="secondary"
                >
                  Back
                </Button>
                <Button
                  onClick={handleConfirm}
                  variant="primary"
                >
                  Confirm Booking
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
