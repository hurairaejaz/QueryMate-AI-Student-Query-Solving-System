"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

export default function UpdateKbPage() {
  const { id } = useParams();
  const router = useRouter();

  const [formData, setFormData] = useState({
    title: "",
    content: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchKbData = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/kb/${id}`);
        const data = await res.json();

        if (!res.ok) {
          setMessage(data.detail || "Failed to load KB data");
          setLoading(false);
          return;
        }

        setFormData({
          title: data.title || "",
          content: data.content || "",
        });
      } catch (error) {
        setMessage("Error loading KB data");
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchKbData();
  }, [id]);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");

    try {
      const body = new FormData();
      body.append("title", formData.title);
      body.append("content", formData.content);

      const res = await fetch(`http://127.0.0.1:8000/kb/${id}`, {
        method: "PUT",
        body,
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail || "Update failed");
        setSaving(false);
        return;
      }

      setMessage("KB updated successfully");
      setTimeout(() => {
        router.push("/admin/kb");
      }, 1000);
    } catch (error) {
      setMessage("Something went wrong while updating");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Update Knowledge Base</h2>

      {message && <p>{message}</p>}

      <form onSubmit={handleUpdate}>
        <div style={{ marginBottom: "10px" }}>
          <label>Title</label>
          <br />
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px" }}
            required
          />
        </div>

        <div style={{ marginBottom: "10px" }}>
          <label>Content</label>
          <br />
          <textarea
            name="content"
            value={formData.content}
            onChange={handleChange}
            rows="6"
            style={{ width: "100%", padding: "10px" }}
            required
          />
        </div>

        <button type="submit" disabled={saving}>
          {saving ? "Updating..." : "Update"}
        </button>
      </form>
    </div>
  );
}