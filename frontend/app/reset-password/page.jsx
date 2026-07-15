"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Lock, User, Key, Eye, EyeOff, ShieldCheck } from "lucide-react"; // Note: Needs 'lucide-react' library

export default function ResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const identifierFromUrl = searchParams.get("identifier") || "";

  const [identifier, setIdentifier] = useState(identifierFromUrl);
  const [otpCode, setOtpCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleReset(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    try {
      if (newPassword !== confirmPassword) {
        throw new Error("Passwords do not match");
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/reset-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            identifier: identifier.trim(),
            otp_code: otpCode.trim(),
            new_password: newPassword,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setMessage(data.message || "Password reset successfully");

      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err) {
      setError(err.message || "Reset failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Branding/Icon */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-2xl shadow-lg mb-4">
            <ShieldCheck size={32} />
          </div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
            Reset Password
          </h1>
          <p className="text-gray-500 mt-2">
            Secure your QueryMate account
          </p>
        </div>

        <div className="bg-white/80 backdrop-blur-sm shadow-2xl rounded-3xl p-8 border border-white">
          <form onSubmit={handleReset} className="space-y-5">
            {/* Identifier Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 ml-1">Email or Phone</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                  <User size={18} />
                </span>
                <input
                  type="text"
                  placeholder="Enter your registered identifier"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  className="w-full pl-11 pr-4 py-3.5 bg-gray-50/50 border border-gray-200 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all placeholder:text-gray-400 text-gray-900"
                  required
                />
              </div>
            </div>

            {/* OTP Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 ml-1">Verification Code</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                  <Key size={18} />
                </span>
                <input
                  type="text"
                  placeholder="Enter the 6-digit OTP"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  className="w-full pl-11 pr-4 py-3.5 bg-gray-50/50 border border-gray-200 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all placeholder:text-gray-400 text-gray-900"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {/* New Password */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1 ml-1">New Password</label>
                <div className="relative">
                  <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                    <Lock size={18} />
                  </span>
                  <input
                    type="password"
                    placeholder="••••••••"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full pl-11 pr-4 py-3.5 bg-gray-50/50 border border-gray-200 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all placeholder:text-gray-400 text-gray-900"
                    required
                  />
                </div>
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1 ml-1">Confirm Password</label>
                <div className="relative">
                  <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                    <Lock size={18} />
                  </span>
                  <input
                    type="password"
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full pl-11 pr-4 py-3.5 bg-gray-50/50 border border-gray-200 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all placeholder:text-gray-400 text-gray-900"
                    required
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-semibold shadow-lg shadow-blue-200 transition-all active:scale-[0.98] disabled:opacity-70 disabled:active:scale-100 flex justify-center items-center"
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </>
              ) : "Reset Password"}
            </button>
          </form>

          {/* Success Message */}
          {message && (
            <div className="mt-6 flex items-center gap-3 text-sm text-green-700 bg-green-50 border border-green-100 rounded-xl p-4 animate-in fade-in slide-in-from-top-2">
              <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
              {message}
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-6 flex items-center gap-3 text-sm text-red-700 bg-red-50 border border-red-100 rounded-xl p-4 animate-in fade-in slide-in-from-top-2">
              <div className="h-2 w-2 bg-red-500 rounded-full" />
              {error}
            </div>
          )}
        </div>
        
        <p className="text-center mt-8 text-sm text-gray-500">
          Remembered your password?{" "}
          <button onClick={() => router.push("/login")} className="text-blue-600 font-semibold hover:underline">
            Back to login
          </button>
        </p>
      </div>
    </div>
  );
}