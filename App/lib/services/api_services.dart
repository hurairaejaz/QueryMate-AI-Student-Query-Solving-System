import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';

class ApiService {
  static String get baseUrl => AppConfig.baseUrl;

  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("access_token");
  }

  static String getFullUrl(String path) {
    if (path.startsWith("http")) return path;
    return "$baseUrl$path";
  }

  static Future<Map<String, String>> _buildHeaders({
    bool authRequired = false,
  }) async {
    final headers = <String, String>{
      "Content-Type": "application/json",
      "Accept": "application/json",
      "ngrok-skip-browser-warning": "true",
    };

    if (authRequired) {
      final token = await _getToken();

      if (token == null || token.isEmpty) {
        throw Exception("No auth token found. Please login again.");
      }

      headers["Authorization"] = "Bearer $token";
    }

    return headers;
  }

  static Future<dynamic> getRequest(
      String endpoint, {
        bool authRequired = false,
      }) async {
    final headers = await _buildHeaders(authRequired: authRequired);

    final response = await http
        .get(
      Uri.parse("$baseUrl$endpoint"),
      headers: headers,
    )
        .timeout(const Duration(seconds: 20));

    return _handleResponse(response);
  }

  static Future<dynamic> postRequest(
      String endpoint, {
        Map<String, dynamic>? body,
        bool authRequired = false,
      }) async {
    final headers = await _buildHeaders(authRequired: authRequired);

    final response = await http
        .post(
      Uri.parse("$baseUrl$endpoint"),
      headers: headers,
      body: jsonEncode(body ?? {}),
    )
        .timeout(const Duration(seconds: 20));

    return _handleResponse(response);
  }

  static Future<dynamic> putRequest(
      String endpoint, {
        Map<String, dynamic>? body,
        bool authRequired = false,
      }) async {
    final headers = await _buildHeaders(authRequired: authRequired);

    final response = await http
        .put(
      Uri.parse("$baseUrl$endpoint"),
      headers: headers,
      body: jsonEncode(body ?? {}),
    )
        .timeout(const Duration(seconds: 20));

    return _handleResponse(response);
  }

  static Future<dynamic> deleteRequest(
      String endpoint, {
        bool authRequired = false,
      }) async {
    final headers = await _buildHeaders(authRequired: authRequired);

    final response = await http
        .delete(
      Uri.parse("$baseUrl$endpoint"),
      headers: headers,
    )
        .timeout(const Duration(seconds: 20));

    return _handleResponse(response);
  }

  static Future<dynamic> postMultipartRequest(
      String endpoint, {
        Map<String, String>? fields,
        String? filePath,
        String fileFieldName = "file",
        bool authRequired = false,
      }) async {
    final uri = Uri.parse("$baseUrl$endpoint");
    final request = http.MultipartRequest("POST", uri);

    final headers = await _buildHeaders(authRequired: authRequired);

    // Multipart request must not use JSON Content-Type.
    headers.remove("Content-Type");

    request.headers.addAll(headers);

    if (fields != null) {
      request.fields.addAll(fields);
    }

    if (filePath != null && filePath.isNotEmpty) {
      request.files.add(
        await http.MultipartFile.fromPath(fileFieldName, filePath),
      );
    }

    final streamedResponse =
    await request.send().timeout(const Duration(seconds: 30));

    final response = await http.Response.fromStream(streamedResponse);

    return _handleResponse(response);
  }

  static dynamic _handleResponse(http.Response response) {
    final statusCode = response.statusCode;
    final responseBody = response.body;

    dynamic decodedBody;

    try {
      decodedBody = responseBody.isNotEmpty ? jsonDecode(responseBody) : null;
    } catch (_) {
      decodedBody = responseBody;
    }

    print("API Response [$statusCode]: $decodedBody");

    if (statusCode >= 200 && statusCode < 300) {
      return decodedBody;
    }

    if (statusCode == 401) {
      throw Exception("Unauthorized. Please login again.");
    }

    if (statusCode == 403) {
      throw Exception("Forbidden. You do not have permission.");
    }

    if (statusCode == 404) {
      throw Exception("API endpoint not found.");
    }

    if (statusCode == 422) {
      throw Exception("Validation error: $decodedBody");
    }

    if (statusCode >= 500) {
      throw Exception("Server error: $decodedBody");
    }

    throw Exception("Request failed [$statusCode]: $decodedBody");
  }
}