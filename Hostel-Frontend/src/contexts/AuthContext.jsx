import { useState, useEffect } from 'react';
import { AuthContext } from './authContextCreate';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) setUser(JSON.parse(savedUser));
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const fakeUser = { email: credentials.email };
      localStorage.setItem("user", JSON.stringify(fakeUser));
      setUser(fakeUser);
    } catch (err) {
      console.error("Login failed:", err);
    }
  };

  const signup = async (data) => {
    try {
      const newUser = { email: data.email };
      localStorage.setItem("user", JSON.stringify(newUser));
      setUser(newUser);
    } catch (err) {
      console.error("Signup failed:", err);
    }
  };

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
