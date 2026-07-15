"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  BookOpen,
  AlertCircle,
  LogOut,
  UserCircle,
} from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { name: "Knowledge Base", href: "/admin/kb", icon: BookOpen },
  { name: "Escalations", href: "/admin/escalated", icon: AlertCircle },
];

export default function AdminLayout({ children }) {
  const router = useRouter();
  const pathname = usePathname();

  const [ok, setOk] = useState(null);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [adminName, setAdminName] = useState("Admin");

  // 🔥 FETCH ADMIN PROFILE (FIXED)
  const fetchAdminProfile = async () => {
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
      console.log("Profile API failed:", res.status);
      setAdminName("Admin");
      return;
    }

    const data = await res.json();

    console.log("ADMIN PROFILE DATA:", data);

    setAdminName(data.full_name || "Admin");

  } catch (err) {
    console.error("Profile fetch error:", err);
    setAdminName("Admin");
  }
};

  // 🔥 LOGOUT
  const handleLogout = async () => {
    if (isLoggingOut) return;
    setIsLoggingOut(true);

    try {
      await fetch(`${API}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
    } catch (e) {
      console.error("Logout error:", e);
    }

    localStorage.removeItem("is_logged_in");
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_email");
    localStorage.removeItem("access_token");

    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 UTC; path=/;";
    document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 UTC; path=/;";
    document.cookie = "user_role=; expires=Thu, 01 Jan 1970 UTC; path=/;";

    router.replace("/login");
  };

  useEffect(() => {
    const checkAuth = () => {
      try {
        const isLoggedIn = localStorage.getItem("is_logged_in");
        const userRole = localStorage.getItem("user_role");

        if (isLoggedIn !== "true" || userRole !== "admin") {
          setOk(false);
          router.replace(`/login`);
          return;
        }

        setOk(true);

        // 🔥 IMPORTANT: CALL PROFILE
        fetchAdminProfile();

      } catch (e) {
        console.error("Auth check error:", e);
        setOk(false);
        router.replace(`/login`);
      }
    };

    checkAuth();
  }, []);

  if (ok === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 text-slate-700">
        Checking session...
      </div>
    );
  }

  if (ok === false) return null;

  return (
    <div className="flex flex-col bg-gray-50 text-slate-900">

      {/* SIDEBAR */}
      <aside className="md:flex w-full md:w-64 bg-slate-900 text-white flex flex-col fixed inset-y-0 shadow-xl">
        <div className="p-8">
          <h1 className="text-2xl font-black text-blue-400 tracking-tighter">
            QueryMate
          </h1>
        </div>

        <nav className="flex-1 px-4 space-y-2">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === "/admin"
                ? pathname === "/admin"
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-4 px-4 py-3 rounded-xl font-bold transition-all ${
                  isActive
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-900/40"
                    : "text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <item.icon size={20} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-6 border-t border-slate-800">
          <button
            onClick={handleLogout}
            className="flex items-center gap-4 text-slate-400 hover:text-red-400 font-bold transition-colors w-full px-4"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* MAIN */}
      <div className="flex-1 md:ml-64 flex flex-col min-w-0">

        {/* HEADER */}
        <header className="h-16 md:h-20 bg-white border-b border-gray-200 px-4 md:px-8 flex items-center justify-between sticky top-0 z-30">

          <div></div>

          <div className="flex items-center gap-4">

            {/*  ADMIN NAME */}
            <div className="text-right">
              <p className="text-[16px] md:text-[20px] font-bold text-blue-600 uppercase">
                {adminName}
              </p>
            </div>

            {/* PROFILE */}
            <Link href="/admin/profile">
              <div className="bg-slate-100 p-2 rounded-full border-2 border-white shadow-sm cursor-pointer hover:bg-blue-100 transition-all">
                <UserCircle className="text-slate-600 hover:text-blue-600" size={28} />
              </div>
            </Link>

          </div>
        </header>

        <main className="p-8 md:p-12">
          <div className="max-w-5xl mx-auto">{children}</div>
        </main>
      </div>
    </div>
  );
}