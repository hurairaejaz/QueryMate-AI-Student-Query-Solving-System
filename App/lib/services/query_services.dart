import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:querymate/config/app_config.dart';
import 'package:querymate/models/query_request.dart';
import 'package:querymate/models/query_response.dart';

class QueryService {
  static Future<QueryResponse> submitQuery(QueryRequest request) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("access_token");

    if (token == null || token.isEmpty) {
      throw Exception("No token found. Please login again.");
    }

    final url = Uri.parse("${AppConfig.baseUrl}/app/query/submit");

    final response = await http.post(
      url,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      body: jsonEncode({
        "query_text": request.queryText,
      }),
    );

    final data = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return QueryResponse.fromJson(data);
    } else {
      throw Exception(data.toString());
    }
  }

  static Future<List<dynamic>> getQueryHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("access_token");

    if (token == null || token.isEmpty) {
      throw Exception("No token found. Please login again.");
    }

    final url = Uri.parse("${AppConfig.baseUrl}/app/query/history");

    final response = await http.get(
      url,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
    );

    final data = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return data;
    } else {
      throw Exception(data.toString());
    }
  }
}