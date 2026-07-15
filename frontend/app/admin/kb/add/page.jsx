"use client";

import React, { useState } from "react";
import { Trash2, Send } from "lucide-react";
import { useRouter } from "next/navigation";
import { apiRequest } from "../../../../lib/apiRequest";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function AddKB() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new FormData();
    
    // Use the state values directly
    formData.append("title", question.trim()); 
    formData.append("question", question.trim());
    formData.append("answer", answer.trim());
    formData.append("language", "en");
    formData.append("department_key", "software_engineering"); // Matches your backend default

    if (file) {
      formData.append("file", file);
    }

    // ONLY ONE REQUEST: Use your helper OR a clean fetch.
    // I will use fetch here to show you the correct way to handle the headers.
    const token = localStorage.getItem("access_token");
    const headers = {};
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API}/admin/kb/`, {
      method: "POST",
      headers: headers, 
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Failed to save knowledge base entry");
    }

    const data = await response.json();
    console.log("Success:", data);
    
    alert("Knowledge added successfully");
    
    // Clear form and redirect AFTER success
    setQuestion("");
    setAnswer("");
    setFile(null);
    router.push("/admin/kb");

  } catch (err) {
    console.error("Submit Error:", err);
    alert(err.message);
    setError(err.message);
  } finally {
    setLoading(false);
  }
  };

  return (
    
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-gray-200 mt-10">
      <div className="flex justify-end mb-4">
        <button
          onClick={() => router.back()}
          className="p-2 rounded-full hover:bg-gray-100 transition"
          title="Close"
        >
          ✕
        </button>
      </div>
      {/* Header - Simple & Clear */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">Add Knowledge</h1>
        <p className="text-lg text-gray-600">Fill in the details below to train your AI.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Question Input */}
        <div>
          <label className="block text-lg font-bold text-gray-800 mb-2">
            The Question
          </label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="What do people usually ask?"
            className="w-full p-4 text-lg border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-0 outline-none transition-colors"
            required
          />
        </div>

        {/* Answer Input */}
        <div>
          <label className="block text-lg font-bold text-gray-800 mb-2">
            The Answer
          </label>
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type the correct response here..."
            className="w-full p-4 text-lg border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-0 outline-none min-h-[150px] transition-colors"
            required
          />
        </div>

        {/* Simple File Upload */}
        <div className="p-4 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <label className="block text-sm font-bold text-gray-500 uppercase mb-2">
            Attachment (Optional)
          </label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {file && (
            <div className="mt-2 flex items-center justify-between bg-white p-2 rounded border border-gray-200">
              <span className="text-blue-600 font-medium">{file.name}</span>
              <button type="button" onClick={() => setFile(null)} className="text-red-500">
                <Trash2 size={18} />
              </button>
            </div>
          )}
        </div>

        {/* Big Blue Button */}
        <div className="flex flex-col gap-3">
          <button
          
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold py-4 rounded-xl transition-all flex items-center justify-center gap-2"
          >
            Save Knowledge <Send size={20} />
          </button>
          
          <button
            type="button"
            onClick={() => {setTitle(""); setQuestion(""); setAnswer(""); setFile(null);}}
            className="text-gray-500 font-semibold hover:text-gray-700 transition-colors"
          >
            Clear everything
          </button>
        </div>

      </form>
    </div>
  );
}