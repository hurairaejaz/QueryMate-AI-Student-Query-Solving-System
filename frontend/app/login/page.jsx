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

export default function LoginPage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${API}/auth/admin/login`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();
      console.log("Login response:", data);

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // Debug: Check cookies after login
      console.log("Login successful, redirecting to /admin...");
      console.log("Response data:", data);
      
      // Store access_token in localStorage for API fallback
      localStorage.setItem("access_token", data.access_token);
      // Store user info in localStorage for reliable session management
      localStorage.setItem("user_role", data.role);
      localStorage.setItem("user_email", formData.email);
      localStorage.setItem("is_logged_in", "true");
      
      // Redirect to admin
      router.replace("/admin");
    } catch (err) {
      console.error("LOGIN ERROR:", err);
      setError(err.message);
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
        className={`relative bg-black/30 backdrop-blur-md border border-[${Colors.Secondary}]/40 rounded-3xl p-8 md:p-12 w-full max-w-sm shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)]`}
      >
        {/* Close Button */}
        <Link
          href="/"
          className={`absolute top-5 right-5 text-[${Colors.TextLight}] hover:text-[${Colors.Accent}] transition`}
        >
          <X size={24} />
        </Link>


        
        <h1
          className={`text-3xl font-extrabold mb-8 text-center text-[${Colors.Accent}]`}
        >
          QueryMate Login
        </h1>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Email */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Email
            </label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
              className={`w-full px-4 py-3 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Password
            </label>

            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              className={`w-full px-4 py-3 rounded-lg bg-white/10 border border-transparent placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-[${Colors.Accent}]`}
            />
          </div>

          {/* Error */}
          {error && (
            <p className="text-red-400 text-sm text-center bg-red-900/30 p-2 rounded-lg">
              {error}
            </p>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            className={`w-full bg-[${Colors.Accent}] hover:bg-[${Colors.Secondary}] text-[${Colors.Primary}] font-extrabold py-3 rounded-lg transition shadow-xl mt-8`}
          >
            Login
          </button>
        <Link
          href="/forgot-password"
          className="text-blue-600 text-sm font-semibold hover:underline"
>
          Forgot Password?
        </Link>
        </form>

        <p className="text-sm text-center mt-8">
          Don’t have an account?{" "}
          <Link
            href="/signup"
            className={`text-[${Colors.Accent}] font-semibold hover:underline`}
          >
            Sign up here
          </Link>
        </p>
      </motion.div>
    </main>
  );
}