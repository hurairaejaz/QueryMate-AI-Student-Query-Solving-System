import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';
import 'api_services.dart';
class AuthService {
  static Future<bool> login({
    required String email,
    required String password,
  }) async {
    final data = await ApiService.postRequest(
      "/auth/login",
      body: {
        "email": email.trim(),
        "password": password.trim(),
      },
      authRequired: false,
    );

    print("LOGIN DATA: $data");

    if (data != null && data["access_token"] != null) {
      final prefs = await SharedPreferences.getInstance();

      await prefs.setString("access_token", data["access_token"]);
      await prefs.setBool("is_logged_in", true);

      // CHANGE: Save user data also because HomeScreen uses these values.
      final user = data["user"];

      if (user != null) {
        await prefs.setString("name", user["full_name"]?.toString() ?? "");
        await prefs.setString("email", user["email"]?.toString() ?? "");
        await prefs.setString("phone", user["phone"]?.toString() ?? "");
        await prefs.setString("role", user["role"]?.toString() ?? "");
        await prefs.setString("user_id", user["user_id"]?.toString() ?? "");
      }

      return true;
    }

    return false;
  }

  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString("access_token", token);
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("access_token");
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.remove("access_token");
    await prefs.remove("name");
    await prefs.remove("email");
    await prefs.remove("phone");
    await prefs.remove("role");
    await prefs.remove("user_id");

    await prefs.setBool("is_logged_in", false);
    // if (!mounted) return;
    // Navigator.pushNamedAndRemoveUntil(
    //   context,
    //   '/login',
    //       (route) => false,
    // );

  }

  static Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }
}