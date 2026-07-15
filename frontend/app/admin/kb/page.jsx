"use client";

import { useRouter } from "next/navigation";
import React, { useState, useEffect } from "react";
import {
  Plus,
  Search,
  FileText,
  Edit,
  Trash2,
  UserCircle,
  Layout,
  Loader2,
  ExternalLink,
  RefreshCcw,
} from "lucide-react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function KBDashboard() {
  const router = useRouter();

  const [kbArticles, setKbArticles] = useState([]);
  const [adminName, setAdminName] = useState("Admin");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const [editForm, setEditForm] = useState({
    title: "",
    content: "",
  });

  const [editFile, setEditFile] = useState(null);

  useEffect(() => {
    fetchKBEntries();
    fetchAdminName();
  }, []);

  const fetchAdminName = async () => {
    try {
      const email = localStorage.getItem("user_email");

      if (!email) {
        setAdminName("Admin");
        return;
      }

      const res = await fetch(
        `${API}/admin/profile/by-email?email=${encodeURIComponent(email)}`
      );

      if (!res.ok) {
        console.log("Admin name API failed:", res.status);
        setAdminName("Admin");
        return;
      }

      const data = await res.json();
      console.log("ADMIN NAME DATA:", data);

      setAdminName(data.full_name || "Admin");
    } catch (err) {
      console.error("Admin name fetch error:", err);
      setAdminName("Admin");
    }
  };

  const fetchKBEntries = async () => {
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");
      const headers = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${API}/admin/kb/?skip=0&limit=1000`, {
        method: "GET",
        credentials: "include",
        headers,
      });

      if (!response.ok) {
        if (response.status === 401) {
          window.location.href = "/login";
          return;
        }
        throw new Error("Failed to fetch data");
      }

      const data = await response.json();

      const transformed = data.map((item) => ({
        id: item.kb_id || item.id,
        title: item.title || item.question || "Untitled",
        content: item.content || "",
        category: item.language || "General",
        lastUpdated: item.updated_at
          ? new Date(item.updated_at).toISOString().split("T")[0]
          : new Date().toISOString().split("T")[0],
        file_url:
          item.file_url ||
          (item.attachments && item.attachments.length > 0
            ? item.attachments[0].file_url
            : null),
        file_name:
          item.file_name ||
          (item.attachments && item.attachments.length > 0
            ? item.attachments[0].file_name
            : null),
      }));

      setKbArticles(transformed);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching KB entries:", err);
    } finally {
      setLoading(false);
    }
  };

  const openEditModal = async (article) => {
    try {
      const token = localStorage.getItem("access_token");
      const headers = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${API}/admin/kb/${article.id}`, {
        method: "GET",
        credentials: "include",
        headers,
      });

      if (!response.ok) {
        throw new Error("Failed to load entry");
      }

      const data = await response.json();

      setSelectedItem({
        id: data.kb_id || data.id,
        title: data.title || "",
        content: data.content || "",
        category:
          data.language || data.category || data.department_key || "General",
        department_key: data.department_key || "software_engineering",
        created_at: data.created_at || null,
        updated_at: data.updated_at || null,
        file_url:
          data.file_url ||
          (data.attachments && data.attachments.length > 0
            ? data.attachments[0].file_url
            : null),
        file_name:
          data.file_name ||
          (data.attachments && data.attachments.length > 0
            ? data.attachments[0].file_name
            : null),
      });

      setEditForm({
        title: data.title || "",
        content: data.content || "",
      });

      setEditFile(null);
      setShowEditModal(true);
    } catch (err) {
      alert("Error loading entry: " + err.message);
    }
  };

  const openDeleteModal = async (article) => {
    try {
      const token = localStorage.getItem("access_token");
      const headers = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${API}/admin/kb/${article.id}`, {
        method: "GET",
        credentials: "include",
        headers,
      });

      if (!response.ok) {
        throw new Error("Failed to load entry");
      }

      const data = await response.json();

      setSelectedItem({
        id: data.kb_id || data.id,
        title: data.title || "",
        content: data.content || "",
        category:
          data.language || data.category || data.department_key || "General",
        department_key: data.department_key || "software_engineering",
        created_at: data.created_at || null,
        updated_at: data.updated_at || null,
        file_url:
          data.file_url ||
          (data.attachments && data.attachments.length > 0
            ? data.attachments[0].file_url
            : null),
        file_name:
          data.file_name ||
          (data.attachments && data.attachments.length > 0
            ? data.attachments[0].file_name
            : null),
      });

      setShowDeleteModal(true);
    } catch (err) {
      alert("Error loading entry: " + err.message);
    }
  };

  const handleUpdate = async () => {
    if (!selectedItem) return;

    try {
      const token = localStorage.getItem("access_token");
      const headers = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const formData = new FormData();
      formData.append("title", editForm.title);
      formData.append("content", editForm.content);

      if (editFile) {
        formData.append("file", editFile);
      }

      const response = await fetch(`${API}/admin/kb/${selectedItem.id}`, {
        method: "PUT",
        credentials: "include",
        headers,
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || "Failed to update entry");
      }

      alert("Entry updated successfully");
      setShowEditModal(false);
      setSelectedItem(null);
      setEditFile(null);
      fetchKBEntries();
    } catch (err) {
      alert("Error updating entry: " + err.message);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!selectedItem) return;

    try {
      const token = localStorage.getItem("access_token");
      const headers = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${API}/admin/kb/${selectedItem.id}`, {
        method: "DELETE",
        credentials: "include",
        headers,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || "Failed to delete entry");
      }

      setKbArticles((prev) =>
        prev.filter((article) => article.id !== selectedItem.id)
      );

      setShowDeleteModal(false);
      setSelectedItem(null);
    } catch (err) {
      alert("Error deleting entry: " + err.message);
    }
  };

  const filteredArticles = kbArticles.filter(
    (article) =>
      article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      article.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-10 text-slate-900 font-sans">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center mb-10 border-b-2 border-slate-200 pb-6 gap-6">
          <div className="flex items-center gap-3">
            <UserCircle size={48} className="text-blue-600" />
            <div>
              <h1 className="text-3xl font-black text-slate-900">
                {adminName}
              </h1>
            </div>
          </div>

          <Link
            href="/admin/kb/add"
            className="w-full md:w-auto bg-blue-600 hover:bg-slate-900 text-white px-8 py-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-100 active:scale-95"
          >
            <Plus size={24} strokeWidth={3} /> Create New Entry
          </Link>
        </div>

        <div className="bg-white border-2 border-slate-100 rounded-3xl md:rounded-[2.5rem] shadow-sm overflow-hidden">
          <div className="p-6 bg-slate-50 border-b-2 border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              {/* <Layout className="text-blue-600" /> */}
              <button 
                 onClick={fetchKBEntries}
                 disabled={loading}
                 className="p-1 hover:bg-blue-100 rounded-full transition-all active:scale-90 disabled:opacity-50"
                 title="Refresh Data"
               >
                 <RefreshCcw 
                   size={20} 
                   className={`text-blue-600 cursor-pointer transition-all hover:text-slate-900 active:scale-90 ${loading ? 'animate-spin' : ''}`} 
                 />
               </button>
              <h2 className="text-xl font-black text-slate-800 uppercase tracking-tight">
                Database Management
              </h2>
            </div>

            <div className="relative w-full md:w-80">
              <Search
                className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
                size={20}
              />
              <input
                type="text"
                placeholder="Find query..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-white border-2 border-slate-200 rounded-xl focus:border-blue-600 outline-none font-bold transition-all"
              />
            </div>
          </div>

          {loading && (
            <div className="p-20 text-center">
              <Loader2
                className="animate-spin mx-auto text-blue-600"
                size={48}
              />
              <p className="mt-4 text-slate-400 font-bold">
                Loading articles...
              </p>
            </div>
          )}

          {error && !loading && (
            <div className="p-20 text-center">
              <p className="text-red-500 font-bold">Error: {error}</p>
              <button
                onClick={fetchKBEntries}
                className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg font-bold"
              >
                Retry
              </button>
            </div>
          )}

          {!loading && !error && (
            <>
              <div className="hidden lg:block overflow-x-auto">
                <table className="w-full text-left table-fixed">
                  <thead>
                    <tr className="text-xm font-black uppercase tracking-widest border-b border-slate-50">
                      <th className="px-8 py-5 w-1/2">Questions</th>
                      <th className="px-8 py-5 w-1/6">Category</th>
                      <th className="px-8 py-5 w-1/6">File</th>
                      <th className="px-8 py-5 w-1/6 text-right">Controls</th>
                    </tr>
                  </thead>

                  <tbody className="divide-y divide-slate-50">
                    {filteredArticles.map((article) => (
                      <tr
                        key={article.id}
                        className="hover:bg-blue-50/50 transition-colors"
                      >
                        <td className="px-8 py-6">
                          <div className="flex items-center gap-4">
                            <div className="p-3 bg-blue-50 text-blue-600 rounded-xl shrink-0">
                              <FileText size={20} />
                            </div>
                            <div className="min-w-0">
                              <p
                                className="font-black text-slate-900 text-lg truncate"
                                title={article.title}
                              >
                                {article.title}
                              </p>
                              <p className="text-sm text-slate-400 font-bold">
                                Updated {article.lastUpdated}
                              </p>
                            </div>
                          </div>
                        </td>

                        <td className="px-8 py-6 font-bold text-slate-500 uppercase text-xs tracking-tighter truncate">
                          {article.category}
                        </td>

                        <td className="px-8 py-6">
                          {article.file_url ? (
                            <div className="flex flex-col gap-1">
                              <p className="text-sm font-bold text-slate-700 truncate max-w-[150px]">
                                {article.file_name || "Attached File"}
                              </p>
                              <a
                                href={article.file_url}
                                target="_blank"
                                rel="noreferrer"
                                className="text-blue-600 font-bold underline text-sm flex items-center gap-1"
                              >
                                Open <ExternalLink size={12} />
                              </a>
                            </div>
                          ) : (
                            <span className="text-slate-400 text-sm font-bold">
                              No File
                            </span>
                          )}
                        </td>

                        <td className="px-8 py-6 text-right">
                          <div className="flex justify-end gap-2">
                            <button
                              onClick={() => openEditModal(article)}
                              className="p-3 text-slate-400 hover:bg-blue-600 hover:text-white rounded-xl transition-all"
                              title="Edit"
                            >
                              <Edit size={20} />
                            </button>
                            <button
                              onClick={() => openDeleteModal(article)}
                              className="p-3 text-slate-400 hover:bg-red-600 hover:text-white rounded-xl transition-all"
                              title="Delete"
                            >
                              <Trash2 size={20} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="lg:hidden divide-y divide-slate-100">
                {filteredArticles.map((article) => (
                  <div
                    key={article.id}
                    className="p-6 hover:bg-blue-50/30 transition-colors"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <span className="bg-blue-100 text-blue-700 text-[10px] px-2 py-1 rounded-md font-black uppercase tracking-wider">
                        {article.category}
                      </span>
                      <div className="flex gap-2">
                        <button
                          onClick={() => openEditModal(article)}
                          className="p-2 text-slate-400 bg-slate-100 rounded-lg"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => openDeleteModal(article)}
                          className="p-2 text-red-400 bg-red-50 rounded-lg"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>

                    <h3 className="font-black text-slate-900 text-lg mb-1 leading-tight">
                      {article.title}
                    </h3>

                    <p className="text-xs text-slate-400 font-bold mb-4">
                      Updated {article.lastUpdated}
                    </p>

                    {article.file_url && (
                      <div className="bg-slate-50 p-3 rounded-xl flex items-center justify-between">
                        <div className="flex items-center gap-2 overflow-hidden">
                          <FileText
                            size={16}
                            className="text-slate-400 shrink-0"
                          />
                          <span className="text-sm font-bold text-slate-600 truncate">
                            {article.file_name || "File"}
                          </span>
                        </div>
                        <a
                          href={article.file_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 text-sm font-black underline shrink-0 ml-2"
                        >
                          View
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}

          {!loading && !error && filteredArticles.length === 0 && (
            <div className="p-20 text-center">
              <p className="text-2xl font-bold text-slate-400">
                No articles found.
              </p>
            </div>
          )}
        </div>

        <div className="mt-10 text-center">
          <p className="text-slate-400 text-xs font-black uppercase tracking-[0.3em]">
            QueryMate Control Panel • University of Gujrat
          </p>
        </div>
      </div>

      {showEditModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-white w-full max-w-2xl rounded-3xl p-6 md:p-8 shadow-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-black mb-6 text-slate-900">
              Update Knowledge Entry
            </h2>

            <div className="bg-slate-50 border-2 border-slate-100 rounded-2xl p-4 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm font-bold">
                <p>
                  <span className="text-slate-400">Category:</span>{" "}
                  {selectedItem?.category}
                </p>
                <p>
                  <span className="text-slate-400">Department:</span>{" "}
                  {selectedItem?.department_key}
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block font-black text-slate-700 mb-2 text-sm uppercase tracking-wider">
                  Title
                </label>
                <input
                  type="text"
                  value={editForm.title}
                  onChange={(e) =>
                    setEditForm((prev) => ({
                      ...prev,
                      title: e.target.value,
                    }))
                  }
                  className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 outline-none focus:border-blue-600 transition-all font-bold"
                />
              </div>

              <div>
                <label className="block font-black text-slate-700 mb-2 text-sm uppercase tracking-wider">
                  Content
                </label>
                <textarea
                  value={editForm.content}
                  onChange={(e) =>
                    setEditForm((prev) => ({
                      ...prev,
                      content: e.target.value,
                    }))
                  }
                  rows={4}
                  className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 outline-none focus:border-blue-600 transition-all font-bold"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block font-black text-slate-700 mb-2 text-sm uppercase tracking-wider">
                    Current File
                  </label>

                  {selectedItem?.file_url ? (
                    <div className="border-2 border-slate-100 rounded-xl px-4 py-3 bg-slate-50">
                      <p className="text-sm font-bold text-slate-700 truncate">
                        {selectedItem.file_name || "Attached File"}
                      </p>

                      <a
                        href={selectedItem.file_url}
                        target="_blank"
                        rel="noreferrer"
                        className="mt-2 inline-flex items-center gap-1 text-blue-600 font-black underline text-sm"
                      >
                        View File <ExternalLink size={14} />
                      </a>
                    </div>
                  ) : (
                    <p className="text-sm text-slate-400 font-bold py-3">
                      No File
                    </p>
                  )}
                </div>

                <div>
                  <label className="block font-black text-slate-700 mb-2 text-sm uppercase tracking-wider">
                    Replace File
                  </label>

                  <div className="border-2 border-slate-100 rounded-xl px-4 py-3 bg-slate-50 flex items-center justify-between">
                    <span className="text-sm font-bold text-slate-600 truncate">
                      {editFile ? editFile.name : "No file chosen"}
                    </span>

                    <label className="cursor-pointer bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-black hover:bg-blue-100 transition-all">
                      Choose File
                      <input
                        type="file"
                        onChange={(e) =>
                          setEditFile(e.target.files[0] || null)
                        }
                        className="hidden"
                      />
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-col md:flex-row justify-end gap-3 mt-8">
              <button
                onClick={() => {
                  setShowEditModal(false);
                  setSelectedItem(null);
                  setEditFile(null);
                }}
                className="order-2 md:order-1 px-8 py-3 rounded-xl bg-slate-100 text-slate-600 font-black hover:bg-slate-200 transition-all"
              >
                Cancel
              </button>

              <button
                onClick={handleUpdate}
                className="order-1 md:order-2 px-8 py-3 rounded-xl bg-blue-600 text-white font-black hover:bg-slate-900 transition-all shadow-lg shadow-blue-100"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}

      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-white w-full max-w-md rounded-3xl p-8 shadow-2xl">
            <div className="w-16 h-16 bg-red-50 text-red-600 rounded-2xl flex items-center justify-center mb-6">
              <Trash2 size={32} />
            </div>

            <h2 className="text-2xl font-black mb-2 text-slate-900">
              Delete Entry?
            </h2>

            <p className="text-slate-500 font-bold mb-6">
              This action cannot be undone. This will permanently remove the
              entry from the database.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <p className="text-sm font-bold">
                <span className="text-slate-400">Department:</span>{" "}
                {selectedItem?.department_key}
              </p>
            </div>

            <div className="bg-slate-50 rounded-2xl p-4 mb-8 border-2 border-slate-100">
              <p className="font-black text-slate-900 truncate">
                {selectedItem?.title}
              </p>
              <p className="text-sm text-slate-500 font-bold truncate mt-1">
                {selectedItem?.content}
              </p>
            </div>

            <div className="bg-slate-50 rounded-2xl p-4 mb-6 border-2 border-slate-100 space-y-4">
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  Attachment
                </p>

                {selectedItem?.file_url ? (
                  <a
                    href={selectedItem.file_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-between gap-2 mt-2 text-blue-600 bg-blue-50 p-3 rounded-xl border border-blue-100 hover:bg-blue-100 transition-all"
                  >
                    <span className="flex items-center gap-2 overflow-hidden">
                      <FileText size={16} />
                      <span className="text-xs font-black truncate">
                        {selectedItem.file_name || "Attached File"}
                      </span>
                    </span>
                    <ExternalLink size={14} />
                  </a>
                ) : (
                  <p className="text-xs text-slate-400 font-bold italic mt-1">
                    No file attached
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  setShowDeleteModal(false);
                  setSelectedItem(null);
                }}
                className="px-6 py-4 rounded-2xl bg-slate-100 text-slate-600 font-black hover:bg-slate-200 transition-all"
              >
                Cancel
              </button>

              <button
                onClick={handleDeleteConfirm}
                className="px-6 py-4 rounded-2xl bg-red-600 text-white font-black hover:bg-red-700 transition-all shadow-lg shadow-red-100"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}