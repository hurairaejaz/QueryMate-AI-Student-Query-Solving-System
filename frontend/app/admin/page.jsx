"use client";

import React, { useState, useEffect } from "react";
import {
  Edit,
  Trash2,
  Search,
  User,
  RefreshCcw,
  Plus,
  Loader2,
  FileText,
  ExternalLink
} from "lucide-react";
import Link from "next/link";
import { apiRequest } from "../../lib/apiRequest";
const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
export default function AdminDashboard() {
  const [queries, setQueries] = useState([]);
  const [stats, setStats] = useState({
  total_queries: 0,
  escalated_queries: 0,
  responded_queries: 0,
  latest_escalated: [],
});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [adminName, setAdminName] = useState("Admin");

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
  fetchDashboardStats();
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
  
        setAdminName(
           data.full_name ||
           data.name ||
           data.username ||
           "Admin"
         );
      } catch (err) {
        console.error("Admin name fetch error:", err);
        setAdminName("Admin");
      }
    };

  const extractQuestionFromContent = (content) => {
    if (!content) return "";
    if (content.includes("Q:") && content.includes("A:")) {
      return content.split("A:")[0].replace("Q:", "").trim();
    }
    return content;
  };

  const transformKBItem = (item, index = 0) => {
    return {
      serial: index + 1,
      id: item.kb_id,
      title: item.title,
      question: extractQuestionFromContent(item.content),
      content: item.content,
      category: item.language || "General",
      attachments: item.attachments || [],
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
    };
  };

  const fetchKBEntries = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await apiRequest("/admin/kb/?skip=0&limit=1000", "GET");
      const items = Array.isArray(data) ? data : data.items || [];
      const transformed = items.map((item, index) => transformKBItem(item, index));
      setQueries(transformed);
    } catch (err) {
      if (err.message.toLowerCase().includes("401") || err.message.toLowerCase().includes("not authenticated")) {
        window.location.href = "/login";
        return;
      }
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const fetchDashboardStats = async () => {
    try {
      const data = await apiRequest("/admin/dashboard/stats", "GET");
      setStats({
        total_queries: data.total_queries || 0,
        escalated_queries: data.escalated_queries || 0,
        responded_queries: data.responded_queries || 0,
        latest_escalated: data.latest_escalated || [],
      });
    } catch (err) {
      console.error("Dashboard stats error:", err.message);
    }
  };
  const openEditModal = async (item) => {
    try {
      const data = await apiRequest(`/admin/kb/${item.id}`, "GET");
      
      setSelectedItem({
        id: data.kb_id || data.id,
        title: data.title || "",
        question: extractQuestionFromContent(data.content),
        content: data.content || "",
        category: data.language || data.category || "General",
        department_key: data.department_key || "software_engineering",
        attachments: data.attachments || [],
        file_name:
          data.file_name ||
          data.attachments?.[0]?.file_name ||
          null,
        file_url:
          data.file_url ||
          data.attachments?.[0]?.file_url ||
          null,
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
  
  const openDeleteModal = async (item) => {
    try {
      const data = await apiRequest(`/admin/kb/${item.id}`, "GET");
      setSelectedItem({
        id: data.kb_id || data.id,
        title: data.title || "",
        question: extractQuestionFromContent(data.content),
        content: data.content || "",
        category: data.language || data.category || "General",
        department_key: data.department_key || "software_engineering",
        attachments: data.attachments || [],
        file_name:
          data.file_name ||
          data.attachments?.[0]?.file_name ||
          null,
        file_url:
          data.file_url ||
          data.attachments?.[0]?.file_url ||
          null,
      });
      setShowDeleteModal(true);
    } catch (err) {
      alert("Error loading entry: " + err.message);
    }
  };

  // const runSearch = async () => {
  //   if (!searchTerm.trim()) { fetchKBEntries(); return; }
  //   setLoading(true);
  //   setError("");
  //   try {
  //     const formData = new FormData();
  //     formData.append("query", searchTerm);
  //     formData.append("department_key", "software_engineering");
  //     const data = await apiRequest("/admin/kb/search", "POST", formData, true);
  //     const items = Array.isArray(data) ? data : data.matches || data.items || [];
  //     const transformed = items.map((item, index) => transformKBItem(item, index));
  //     setQueries(transformed);
  //   } catch (err) {
  //     setError(err.message);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  const filteredQueries = queries.filter(
  (q) =>
    q.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.category.toLowerCase().includes(searchTerm.toLowerCase())
);

  const handleUpdate = async () => {
    if (!selectedItem) return;
    try {
      const formData = new FormData();
      formData.append("title", editForm.title);
      formData.append("content", editForm.content);
      if (editFile) formData.append("file", editFile);
      await apiRequest(`/admin/kb/${selectedItem.id}`, "PUT", formData, true);
      setShowEditModal(false);
      setSelectedItem(null);
      fetchKBEntries();
    } catch (err) {
      alert("Error updating entry: " + err.message);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!selectedItem) return;
    try {
      await apiRequest(`/admin/kb/${selectedItem.id}`, "DELETE");
      setShowDeleteModal(false);
      setSelectedItem(null);
      fetchKBEntries();
    } catch (err) {
      alert("Error deleting entry: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-white p-4 md:p-10 text-slate-900 font-sans">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center border-b-4 border-slate-900 pb-6 mb-10 gap-4">
          <div className="flex items-center gap-4">
            <div className="bg-slate-900 text-white p-3 rounded-full shrink-0">
              <User size={30} />
            </div>
           <h1 className="text-2xl md:text-4xl font-black uppercase tracking-tighter">
             {adminName}
           </h1>
          </div>
          <Link href="/admin/kb/add" className="w-full md:w-auto bg-blue-600 hover:bg-black text-white px-6 py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-all">
            <Plus size={20} /> Add Knowledge
          </Link>
        </div>
        {/* DASHBOARD STATS */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">

          {/* TOTAL USER QUERIES */}
          <div className="bg-linear-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-2xl p-5 shadow-sm">
            <p className="text-xs font-black text-blue-600 uppercase tracking-widest">
              Total Queries all time
            </p>
            <h2 className="text-4xl font-black text-slate-900 mt-2">
              {stats.total_queries}
            </h2>
          </div>

          {/* TOTAL KB ENTRIES (IMPORTANT FIX) */}
          <div className="bg-linear-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-2xl p-5 shadow-sm">
            <p className="text-xs font-black text-purple-600 uppercase tracking-widest">
              Number of Added Queries
            </p>
            <h2 className="text-4xl font-black text-slate-900 mt-2">
              {queries.length}
            </h2>
          </div>

          {/* ESCALATED WITH ALERT + LINK */}
          <Link href="/admin/escalated">
            <div className="relative cursor-pointer bg-linear-to-br from-red-50 to-red-100 border border-red-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all">

              {/* ALERT DOT */}
              {stats.escalated_queries > 0 && (
                <span className="absolute top-3 right-3 h-3 w-3 bg-red-600 rounded-full animate-pulse"></span>
              )}

              <p className="text-xs font-black text-red-600 uppercase tracking-widest">
                Total Escalated Queries
              </p>

              <h2 className="text-4xl font-black text-slate-900 mt-2">
                {stats.escalated_queries}
              </h2>

              <p className="text-xs text-red-500 font-bold mt-2">
                Click to respond →
              </p>
            </div>
          </Link>

          {/* RESPONDED */}
          <div className="bg-linear-to-br from-green-50 to-green-100 border border-green-200 rounded-2xl p-5 shadow-sm">
            <p className="text-xs font-black text-green-600 uppercase tracking-widest">
              Total Responded Queries
            </p>
            <h2 className="text-4xl font-black text-slate-900 mt-2">
              {stats.responded_queries}
            </h2>
          </div>

        </div>
        <div className="bg-slate-50 border-2 border-slate-200 rounded-3xl overflow-hidden shadow-sm">
          <div className="p-4 md:p-6 bg-slate-100 border-b-2 border-slate-200 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <h2 className="text-xl md:text-2xl font-black flex items-center gap-2">
              <RefreshCcw className="text-blue-600 cursor-pointer" onClick={fetchKBEntries} />
              Manage Knowledge Base
            </h2>
            <div className="flex flex-1 items-center gap-2 w-full max-w-2xl">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input
                  type="text"
                  placeholder="Search queries..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
  // Removed: onKeyDown={(e) => e.key === "Enter" && runSearch()}
                  className="w-full pl-10 pr-4 py-2 border-2 border-slate-300 rounded-xl focus:border-blue-600 outline-none font-bold"
                />
              </div>
              {/* <button onClick={runSearch} className="bg-blue-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-black transition-all">Search</button> */}
            </div>
          </div>
          
          {loading ? (
            <div className="p-20 text-center">
              <Loader2 className="animate-spin mx-auto text-blue-600" size={48} />
              <p className="mt-4 text-slate-400 font-bold">Loading entries...</p>
            </div>
          ) : error ? (
            <div className="p-20 text-center">
              <p className="text-red-500 font-bold">Error: {error}</p>
              <button onClick={fetchKBEntries} className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg font-bold">Retry</button>
            </div>
          ) : queries.length > 0 ? (
            <>
              {/* DESKTOP TABLE VIEW */}
              <div className="hidden lg:block">
                <table className="w-full text-left border-collapse table-fixed">
                  <thead>
                    <tr className="bg-slate-900 text-white uppercase text-xs tracking-widest">
                      <th className="px-6 py-4 w-16">#</th>
                      <th className="px-6 py-4 w-1/2">Entry Details</th>
                      <th className="px-6 py-4 w-1/6">Category</th>
                      <th className="px-6 py-4 w-1/6">File</th>
                      <th className="px-6 py-4 w-1/6 text-center">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y-2 divide-slate-100">
                    {filteredQueries.map((q) => (
                      <tr key={q.id} className="hover:bg-blue-50 transition-colors">
                        <td className="px-6 py-5 font-black text-slate-400">{q.serial}</td>
                        <td className="px-6 py-5">
                          <p className="font-bold text-lg text-slate-800 truncate" title={q.title}>{q.title}</p>
                          <p className="text-sm text-slate-500 font-medium line-clamp-2 mt-1" title={q.content}>
                            {q.content}
                          </p>
                        </td>
                        <td className="px-6 py-5">
                          <span className="bg-white border border-slate-300 px-3 py-1 rounded-md text-[10px] font-black text-slate-600 uppercase">
                            {q.category}
                          </span>
                        </td>
                        <td className="px-6 py-5">
                          {q.file_url ? (
                            <a href={q.file_url} target="_blank" rel="noreferrer" className="text-blue-600 font-bold underline text-sm truncate block">
                              View File
                            </a>
                          ) : (
                            <span className="text-slate-400 text-sm italic">None</span>
                          )}
                        </td>
                        <td className="px-6 py-5">
                          <div className="flex justify-center gap-2">
                            <button onClick={() => openEditModal(q)} className="p-2 text-blue-600 hover:bg-blue-600 hover:text-white rounded-lg transition-all"><Edit size={18} /></button>
                            <button onClick={() => openDeleteModal(q)} className="p-2 text-red-600 hover:bg-red-600 hover:text-white rounded-lg transition-all"><Trash2 size={18} /></button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* MOBILE CARD VIEW */}
              <div className="lg:hidden divide-y divide-slate-200">
                {filteredQueries.map((q) => (
                  <div key={q.id} className="p-5 hover:bg-blue-50/50">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-[10px] font-black bg-slate-200 px-2 py-1 rounded uppercase">{q.category}</span>
                      <div className="flex gap-2">
                         <button onClick={() => openEditModal(q)} className="p-2 text-blue-600"><Edit size={18} /></button>
                         <button onClick={() => openDeleteModal(q)} className="p-2 text-red-600"><Trash2 size={18} /></button>
                      </div>
                    </div>
                    <h3 className="font-bold text-slate-900 leading-tight mb-1">{q.title}</h3>
                    <p className="text-sm text-slate-500 line-clamp-3 mb-3">{q.content}</p>
                    {q.file_url && (
                      <a href={q.file_url} target="_blank" rel="noreferrer" className="text-blue-600 text-xs font-bold underline flex items-center gap-1">
                        View Attached File <ExternalLink size={12} />
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="p-20 text-center">
              <p className="text-2xl font-bold text-slate-400">No entries found.</p>
            </div>
          )}
        </div>

        <p className="mt-8 text-center text-slate-400 font-bold text-sm uppercase tracking-widest">
          QueryMate Management System • Version 1.0
        </p>
      </div>

      {/* EDIT MODAL */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-white w-full max-w-2xl rounded-2xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Update Knowledge Entry</h2>
            <p className="text-sm font-bold">
                <span className="text-slate-400">Department:</span> {selectedItem?.department_key}
              </p>
            <div className="space-y-4">
              <div>
                <label className="block font-bold mb-2">Title</label>
                <input type="text" value={editForm.title} onChange={(e) => setEditForm((prev) => ({ ...prev, title: e.target.value }))} className="w-full border-2 border-slate-300 rounded-xl px-4 py-3 outline-none" />
              </div>
              <div>
                <label className="block font-bold mb-2">Content</label>
                <textarea value={editForm.content} onChange={(e) => setEditForm((prev) => ({ ...prev, content: e.target.value }))} rows={6} className="w-full border-2 border-slate-300 rounded-xl px-4 py-3 outline-none" />
              </div>
              <div>
                <label className="block font-bold mb-2 text-sm uppercase">Current File</label>
                {selectedItem?.file_url ? (
                  <div className="border-2 border-slate-100 rounded-xl p-3 bg-slate-50 flex items-center justify-between">
                  <span className="font-semibold text-sm text-slate-600 truncate max-w-[200px]">
                    {selectedItem.file_name}
                  </span>

                  <a
                    href={selectedItem.file_url}
                    target="_blank"
                    rel="noreferrer"
                    className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-bold hover:bg-blue-100 transition-all"
                  >
                    Open
                  </a>
                </div>
                ) : <p className="text-slate-400 text-sm italic">No file attached</p>}
              </div>
              {/* CHANGE: Replace File UI same size/style as Current File */}
              <div>
                <label className="block font-bold mb-2 text-sm uppercase">
                  Replace File
                </label>

                <div className="border-2 border-slate-100 rounded-xl p-3 bg-slate-50 flex items-center justify-between">
    
                  {/* Selected file name */}
                  <span className="font-semibold text-sm text-slate-600 truncate max-w-[200px]">
                    {editFile ? editFile.name : "No file chosen"}
                  </span>

                  {/* Styled button */}
                  <label className="cursor-pointer bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-bold hover:bg-blue-100 transition-all">
                    Choose File
                    <input
                      type="file"
                      onChange={(e) => setEditFile(e.target.files[0] || null)}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-8">
              <button onClick={() => { setShowEditModal(false); setSelectedItem(null); }} className="px-6 py-2 rounded-xl bg-slate-100 font-bold">Cancel</button>
              <button onClick={handleUpdate} className="px-6 py-2 rounded-xl bg-blue-600 text-white font-bold">Save Changes</button>
            </div>
          </div>
        </div>
      )}

      {/* DELETE MODAL */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-white w-full max-w-md rounded-2xl p-8 shadow-2xl">
            <h2 className="text-2xl font-bold mb-4 text-red-600">Delete Entry?</h2>
            <p className="text-slate-500 mb-6 font-medium">Are you sure you want to remove this entry? This action cannot be undone.</p>
            <div className="bg-slate-50 border-2 border-slate-100 rounded-xl p-4 mb-8">
              <p className="text-sm font-bold">
                <span className="text-slate-400">Department:</span> {selectedItem?.department_key}
              </p>
              <p className="font-black text-slate-800 truncate">{selectedItem?.title}</p>
              <p className="text-xs text-slate-500 mt-1 line-clamp-1">{selectedItem?.content}</p>
            </div>
            {/* CHANGE: show file in delete popup with same UI */}
            <div className="mb-6">
            <p className="text-xs font-bold text-slate-400 uppercase mb-2">
             Attachment
             </p>

        {selectedItem?.file_url ? (
           <div className="border-2 border-slate-100 rounded-xl p-3 bg-slate-50 flex items-center justify-between">
      
          <span className="text-sm font-semibold text-slate-600 truncate max-w-[200px]">
            {selectedItem.file_name}
          </span>

           <a
            href={selectedItem.file_url}
            target="_blank"
            rel="noreferrer"
            className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-bold hover:bg-blue-100 transition-all"
            >
          View
          </a>
          </div>
          ) : (
          <p className="text-slate-400 text-sm italic">No file attached</p>
           )}
           </div>
            <div className="grid grid-cols-2 gap-3">
              <button onClick={() => { setShowDeleteModal(false); setSelectedItem(null); }} className="px-5 py-3 rounded-xl bg-slate-100 font-bold">Cancel</button>
              <button onClick={handleDeleteConfirm} className="px-5 py-3 rounded-xl bg-red-600 text-white font-bold">Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}