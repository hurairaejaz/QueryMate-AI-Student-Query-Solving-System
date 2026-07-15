"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "../../../lib/apiRequest";
import { RefreshCcw, Search, MessageSquare, UserPlus } from "lucide-react";
const STAFF_MEMBERS = [
  { user_id: 2, name: "Huraira Ejaz", email: "hurairaejaz221@gmail.com" },
  { user_id: 3, name: "Syed Wali", email: "memerhuyrr444@gmail.com" },
  { user_id: 4, name: "Ali Raza", email: "ch.aliraza3182@gmail.com" },
  { user_id: 4, name: "Ms. Hira Noor", email: "hira.noor@uog.edu.pk" },
];

export default function EscalatedPage() {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const [respondModalOpen, setRespondModalOpen] = useState(false);
  const [assignModalOpen, setAssignModalOpen] = useState(false);

  const [selectedQuery, setSelectedQuery] = useState(null);
  const [responseText, setResponseText] = useState("");
  const [selectedStaff, setSelectedStaff] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [responseFile, setResponseFile] = useState(null);
  useEffect(() => {
    fetchEscalatedQueries();
  }, []);
  const handleRefresh = async () => {
    await fetchEscalatedQueries();
   };
  async function fetchEscalatedQueries() {
  try {
    setLoading(true);

    const data = await apiRequest("/admin/escalations/");

    if (Array.isArray(data)) {
      setQueries(data);
    } else if (Array.isArray(data.items)) {
      setQueries(data.items);
    } else if (Array.isArray(data.data)) {
      setQueries(data.data);
    } else if (Array.isArray(data.queries)) {
      setQueries(data.queries);
    } else {
      console.log("Unexpected escalations response:", data);
      setQueries([]);
    }

    setError("");
  } catch (err) {
    setError(err.message || "Failed to load escalated queries");
  } finally {
    setLoading(false);
  }
}

  function openRespondModal(query) {
    setSelectedQuery(query);
    setResponseText(query.response_text || "");
    setRespondModalOpen(true);
  }

  function closeRespondModal() {
    setRespondModalOpen(false);
    setSelectedQuery(null);
    setResponseText("");
    setResponseFile(null);
  }

  function openAssignModal(query) {
    setSelectedQuery(query);
    setSelectedStaff("");
    setAssignModalOpen(true);
  }

  function closeAssignModal() {
    setAssignModalOpen(false);
    setSelectedQuery(null);
    setSelectedStaff("");
  }

  async function handleRespondSubmit(e) {
    e.preventDefault();

    if (!responseText.trim()) {
      alert("Please write a response first.");
      return;
    }

    try {
      setSubmitting(true);

      const formData = new FormData();
      formData.append("response_text", responseText);

      if (responseFile) {
        formData.append("file", responseFile);
      }

      await apiRequest(
        `/admin/escalations/${selectedQuery.query_id}/respond`,
        "POST",
        formData,
        true
      );

      const respondedId = selectedQuery.query_id;
      closeRespondModal();
      setQueries((prev) =>
        prev.filter((q) => q.query_id !== respondedId)
      );
      alert("Response submitted successfully.");
    } catch (err) {
      alert(err.message || "Failed to submit response.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleAssignSubmit(e) {
  e.preventDefault();

  if (!selectedStaff) {
    alert("Please select a staff member.");
    return;
  }

  // CHANGE: Find full selected staff object so we can send email/name to backend.
  const staff = STAFF_MEMBERS.find(
    (member) => member.user_id === Number(selectedStaff)
  );

  if (!staff) {
    alert("Selected staff member not found.");
    return;
  }

  try {
    setSubmitting(true);

    // CHANGE: Send assigned_to_email and assigned_to_name also.
    // Backend needs these values to send email to selected staff.
    await apiRequest(
      `/admin/escalations/${selectedQuery.query_id}/assign`,
      "POST",
      {
        assigned_to: Number(selectedStaff),
        assigned_to_email: staff.email,
        assigned_to_name: staff.name,
        notes: null,
      }
    );

    const assignedId = selectedQuery.query_id;

    closeAssignModal();

    // CHANGE: Update UI with selected staff details immediately.
    setQueries((prev) =>
      prev.map((q) =>
        q.query_id === assignedId
          ? {
              ...q,
              status: "Assigned",
              assigned_to: Number(selectedStaff),
              assigned_to_name: staff.name,
              assigned_to_email: staff.email,
            }
          : q
      )
    );

    alert("Query assigned successfully. Email sent to student and selected staff.");
  } catch (err) {
    alert(err.message || "Failed to assign query.");
  } finally {
    setSubmitting(false);
  }
}

  const filteredQueries = queries.filter((query) => {
    const value = searchTerm.toLowerCase();
    return (
      (query.student_name || "").toLowerCase().includes(value) ||
      (query.student_email || "").toLowerCase().includes(value) ||
      (query.query_text || "").toLowerCase().includes(value) ||
      (query.status || "").toLowerCase().includes(value) ||
      (query.category || "").toLowerCase().includes(value) ||
      (query.source || "").toLowerCase().includes(value)
    );
   
  });

  return (
    <div className="min-h-screen bg-[#f5f7fb] p-4 md:p-6">
      <div className="mx-auto max-w-7xl">
        <div className="rounded-3xl bg-white p-5 md:p-7 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <button
          onClick={handleRefresh}
          disabled={loading}
          className="p-2 rounded-xl hover:bg-gray-100 transition-all active:scale-90 disabled:opacity-50"
          title="Refresh Queries"
        >
          <RefreshCcw 
            size={20} 
            className={`text-blue-600 cursor-pointer transition-all hover:text-slate-900 active:scale-90 ${loading ? 'animate-spin' : ''}`} 
          />
        </button>
           <h1 className="text-2xl md:text-4xl font-bold text-[#183153]">
             Escalated Queries
           </h1>

         </div>
          <p className="mt-2 text-sm md:text-lg text-gray-600 max-w-3xl">
            View escalated queries, respond to students, or assign tasks to staff members.
          </p>

          {/* <div className="mt-5">
            <input
              type="text"
              placeholder="Search by student, email, query, category, or status..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm outline-none focus:border-blue-500 focus:bg-white"
            />
          </div> */}
        </div>

        <div className="mt-6 grid gap-4">
          {loading ? (
            <div className="rounded-3xl bg-white p-8 text-center shadow-sm border border-gray-100">
              <p className="text-gray-500">Loading escalated queries...</p>
            </div>
          ) : error ? (
            <div className="rounded-3xl bg-white p-8 text-center shadow-sm border border-gray-100">
              <p className="text-red-500">{error}</p>
            </div>
          ) : filteredQueries.length === 0 ? (
            <div className="rounded-3xl bg-white p-8 text-center shadow-sm border border-gray-100">
              <p className="text-gray-500">No escalated queries found.</p>
            </div>
          ) : (
            filteredQueries.map((query) => (
              <div
                key={query.query_id}
                className="rounded-3xl bg-white p-5 md:p-6 shadow-sm border border-gray-100"
              >
                <div className="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
                  <div className="flex-1">
                    <div className="flex flex-wrap gap-2">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          query.status === "Escalated"
                            ? "bg-red-100 text-red-700"
                            : query.status === "Assigned"
                            ? "bg-blue-100 text-blue-700"
                            : "bg-green-100 text-green-700"
                        }`}
                      >
                        {query.status}
                      </span>

                      <span className="rounded-full bg-purple-100 px-3 py-1 text-xs font-semibold text-purple-700">
                        {query.category}
                      </span>

                      <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-700">
                        {query.source}
                      </span>
                    </div>

                    <div className="mt-4">
                      <h2 className="text-lg md:text-xl font-bold text-[#183153]">
                        Query #{query.query_id}
                      </h2>
                      <p className="mt-3 text-sm md:text-base leading-7 text-gray-700">
                        {query.query_text}
                      </p>
                    </div>

                    <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                      <div className="rounded-2xl bg-gray-50 p-3">
                        <p className="text-xs font-semibold text-gray-500">Student Name</p>
                        <p className="mt-1 text-sm font-medium text-gray-800">{query.student_name}</p>
                      </div>

                      <div className="bg-slate-50 rounded-2xl p-4">
                       <p className="text-sm font-bold text-slate-500">
                         Contact
                       </p>

                       <p className="font-medium text-slate-900">
                         {query.student_email && query.student_email !== "N/A"
                           ? query.student_email
                           : query.whatsapp_phone
                           ? `WhatsApp: +${query.whatsapp_phone}`
                           : "N/A"}
                       </p>
                     </div>

                      <div className="rounded-2xl bg-gray-50 p-3">
                        <p className="text-xs font-semibold text-gray-500">Created At</p>
                        <p className="mt-1 text-sm font-medium text-gray-800">{query.created_at}</p>
                      </div>

                      <div className="rounded-2xl bg-gray-50 p-3 sm:col-span-2 xl:col-span-3">
                        <p className="text-xs font-semibold text-gray-500">Assigned To</p>
                        <p className="mt-1 text-sm font-medium text-gray-800">
                          {query.assigned_to_name
                            ? `${query.assigned_to_name} (${query.assigned_to_email})`
                            : "Not assigned yet"}
                        </p>
                      </div>

                      {query.response_text && (
                        <div className="rounded-2xl bg-green-50 p-3 sm:col-span-2 xl:col-span-3 border border-green-100">
                          <p className="text-xs font-semibold text-green-700">Latest Response</p>
                          <p className="mt-2 text-sm text-gray-800 leading-6">{query.response_text}</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex flex-col gap-3 sm:flex-row xl:flex-col xl:w-[180px]">
                    <button
                      onClick={() => openRespondModal(query)}
                      className="rounded-2xl bg-green-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-green-700"
                    >
                      Respond
                    </button>

                    <button
                      onClick={() => openAssignModal(query)}
                      className="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
                    >
                      Assign
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {respondModalOpen && (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4 py-6">
    {/* Added max-h and overflow-y-auto to the container */}
    <div className="w-full max-w-2xl rounded-3xl bg-white p-5 md:p-8 shadow-xl max-h-[90vh] overflow-y-auto">
      
      <div className="sticky top-0 bg-white pb-4 flex items-start justify-between gap-4 z-10">
        <div>
          <h2 className="text-xl md:text-2xl font-bold text-[#183153]">Respond to Query</h2>
          <p className="mt-1 text-sm text-gray-500">Query #{selectedQuery?.query_id}</p>
        </div>
        <button
          onClick={closeRespondModal}
          className="rounded-full bg-gray-100 p-2 text-gray-600 hover:bg-gray-200 transition-colors"
        >
          <span className="block w-5 h-5 flex items-center justify-center font-bold">✕</span>
        </button>
      </div>

      <div className="mt-4 rounded-2xl bg-gray-50 p-4 border border-gray-100">
        <p className="text-xs font-bold text-gray-400 uppercase mb-2">Original Query</p>
        <p className="text-sm leading-7 text-gray-700">{selectedQuery?.query_text}</p>
      </div>

      <form onSubmit={handleRespondSubmit} className="mt-5">
        <label className="mb-2 block text-sm font-semibold text-gray-700">Write Response</label>
        <textarea
          rows={6}
          value={responseText}
          onChange={(e) => setResponseText(e.target.value)}
          placeholder="Write a proper response for the student..."
          className="w-full rounded-2xl border border-gray-200 bg-white p-4 text-sm outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100 transition-all"
        />
        
        <label className="mt-4 mb-2 block text-sm font-semibold text-gray-700">
           Attach Document / File
        </label>
        <input
          type="file"
          onChange={(e) => setResponseFile(e.target.files?.[0] || null)}
          className="w-full rounded-2xl border border-gray-200 bg-gray-50 p-3 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
        />

        <div className="mt-8 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={closeRespondModal}
            className="rounded-2xl border border-gray-300 px-8 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>

          <button
            type="submit"
            disabled={submitting}
            className="rounded-2xl bg-green-600 px-8 py-3 text-sm font-semibold text-white hover:bg-green-700 disabled:opacity-50 shadow-md shadow-green-100"
          >
            {submitting ? "Submitting..." : "Submit Response"}
          </button>
        </div>
      </form>
    </div>
  </div>
)}

      {assignModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4 py-6">
          <div className="w-full max-w-lg rounded-3xl bg-white p-5 md:p-6 shadow-xl">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-xl md:text-2xl font-bold text-[#183153]">Assign Query</h2>
                <p className="mt-1 text-sm text-gray-500">Query #{selectedQuery?.query_id}</p>
              </div>

              <button
                onClick={closeAssignModal}
                className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600 hover:bg-gray-200"
              >
                X
              </button>
            </div>

            <form onSubmit={handleAssignSubmit} className="mt-5">
              <label className="mb-2 block text-sm font-semibold text-gray-700">Select Staff Member</label>

              <select
                value={selectedStaff}
                onChange={(e) => setSelectedStaff(e.target.value)}
                className="w-full rounded-2xl border border-gray-200 bg-white p-4 text-sm outline-none focus:border-blue-500"
              >
                <option value="">Choose a staff member</option>
                {STAFF_MEMBERS.map((member) => (
                  <option key={member.user_id} value={member.user_id}>
                    {member.name} - {member.email}
                  </option>
                ))}
              </select>

              <div className="mt-5 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={closeAssignModal}
                  className="rounded-2xl border border-gray-300 px-5 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={submitting}
                  className="rounded-2xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
                >
                  {submitting ? "Assigning..." : "Assign Task"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}