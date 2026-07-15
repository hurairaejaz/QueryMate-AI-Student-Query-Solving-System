"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

export default function DeleteKbPage() {
  const { id } = useParams();
  const router = useRouter();

  const [kbData, setKbData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
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

        setKbData(data);
      } catch (error) {
        setMessage("Error loading KB data");
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchKbData();
  }, [id]);

  const handleDelete = async () => {
    setDeleting(true);
    setMessage("");

    try {
      const res = await fetch(`http://127.0.0.1:8000/kb/${id}`, {
        method: "DELETE",
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail || "Delete failed");
        setDeleting(false);
        return;
      }

      setMessage("KB deleted successfully");
      setTimeout(() => {
        router.push("/admin/kb");
      }, 1000);
    } catch (error) {
      setMessage("Something went wrong while deleting");
    } finally {
      setDeleting(false);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Delete Knowledge Base</h2>

      {message && <p>{message}</p>}

      {kbData && (
        <div style={{ marginBottom: "20px" }}>
          <p><strong>Title:</strong> {kbData.title}</p>
          <p><strong>Content:</strong> {kbData.content}</p>
        </div>
      )}

      <button onClick={handleDelete} disabled={deleting}>
        {deleting ? "Deleting..." : "Confirm Delete"}
      </button>
    </div>
  );
}