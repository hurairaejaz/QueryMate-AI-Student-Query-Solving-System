"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { X } from "lucide-react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const Colors = {
  Primary: "#0C164D",
  Secondary: "#0D9488",
  Accent: "#34D399",
  Background: "#F4F9FF",
  TextDark: "#1F2937",
  TextLight: "#E5E7EB",
};

export default function SignupPage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match!");
      return;
    }

    if (!formData.phone) {
      setError("Phone number is required!");
      return;
    }

    try {
      const response = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: formData.name,
          email: formData.email,
          phone: formData.phone,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed.");
      }

      setSuccess(true);
      alert("Account created successfully! Now login.");
      router.push("/login");
    } catch (err) {
      setError(err.message || "Cannot connect to server. Is backend running?");
    }
  };

  return (
    <main 
      className={`min-h-screen flex items-center justify-center bg-linear-to-br from-[${Colors.Primary}] to-[#1A3172] text-[${Colors.TextLight}] px-4`}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className={`relative bg-black/30 backdrop-blur-md border border-[${Colors.Secondary}]/40 rounded-3xl p-8 md:p-10 w-full max-w-md shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)]`}
      >
        <Link
          href="/"
          className={`absolute top-5 right-5 text-[${Colors.TextLight}] hover:text-[${Colors.Accent}] transition`}
        >
          <X size={24} />
        </Link>

        <h1 className={`text-3xl font-extrabold mb-8 text-center text-[${Colors.Accent}]`}>
          Create a QueryMate Account
        </h1>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-2">Full Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your full name"
              className={`w-full px-4 py-2 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              className={`w-full px-4 py-2 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Phone Number</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Enter phone number"
              className={`w-full px-4 py-2 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Create a password"
              className={`w-full px-4 py-2 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm password"
              className={`w-full px-4 py-2 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
              required
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm font-semibold text-center bg-red-900/30 p-2 rounded-lg">
              {error}
            </p>
          )}

          {success && (
            <p className="text-green-400 text-sm font-semibold text-center bg-green-900/30 p-2 rounded-lg">
              Account created successfully.
            </p>
          )}

          <button
            type="submit"
            className={`w-full bg-[${Colors.Accent}] hover:bg-[${Colors.Secondary}] text-[${Colors.Primary}] font-extrabold py-3 rounded-lg transition shadow-xl mt-4`}
          >
            Sign Up
          </button>
        </form>

        <p className="text-sm text-center mt-8">
          Already have an account?{" "}
          <Link 
            href="/login" 
            className={`text-[${Colors.Accent}] font-semibold hover:underline`}
          >
            Login here
          </Link>
        </p>
      </motion.div>
    </main>
  ); 
}