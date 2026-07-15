import { NextResponse } from "next/server";

export function middleware(req) {
  const role = req.cookies.get("user_role")?.value;
  const { pathname } = req.nextUrl;

  // Don't redirect if already on login, signup, or home page
  if (pathname === "/login" || pathname === "/signup" || pathname === "/") {
    return NextResponse.next();
  }

  // For admin routes, check if user has admin role
  if (pathname.startsWith("/admin")) {
    // If role is not exactly "admin", redirect to login
    if (role !== "admin") {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
