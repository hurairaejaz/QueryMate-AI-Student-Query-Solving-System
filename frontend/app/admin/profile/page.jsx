"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "../../../lib/apiRequest";

export default function AdminProfile() {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
  });

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await apiRequest("/admin/profile/", "GET");

      setForm({
        full_name: data.full_name || "",
        email: data.email || "",
        phone: data.phone || "",
        password: "",
      });
    } catch (err) {
      alert("Error loading profile");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    try {
      await apiRequest("/admin/profile/", "PUT", form);

      setMessage("Profile updated successfully");
      setForm((prev) => ({ ...prev, password: "" }));
    } catch (err) {
      alert("Update failed: " + err.message);
    }
  };

  if (loading) return <p className="p-10">Loading...</p>;

  return (
    <div className="min-h-screen bg-white p-6 md:p-10">
      <div className="max-w-xl mx-auto bg-slate-50 p-6 rounded-2xl border shadow-sm">

        <h1 className="text-2xl font-black mb-6">Admin Profile</h1>

        {message && (
          <p className="bg-green-100 text-green-700 p-3 rounded mb-4 font-bold">
            {message}
          </p>
        )}

        <div className="space-y-4">

          <input
            type="text"
            placeholder="Full Name"
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            className="w-full border-2 p-3 rounded-xl"
          />

          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="w-full border-2 p-3 rounded-xl"
          />

          <input
            type="text"
            placeholder="Phone"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
            className="w-full border-2 p-3 rounded-xl"
          />

          <input
            type="password"
            placeholder="New Password (optional)"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            className="w-full border-2 p-3 rounded-xl"
          />

          <button
            onClick={handleUpdate}
            className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-black transition"
          >
            Update Profile
          </button>

        </div>
      </div>
    </div>
  );
}