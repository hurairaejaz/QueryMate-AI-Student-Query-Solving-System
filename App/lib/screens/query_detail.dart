import 'package:flutter/material.dart';

class QueryDetailScreen extends StatelessWidget {
  final Map<String, dynamic> query;

  const QueryDetailScreen({
    super.key,
    required this.query,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Query Details"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            const Text(
              "Your Query",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(query["query_text"] ?? "No query text"),

            const SizedBox(height: 20),

            const Text(
              "Answer",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(query["answer"] ?? query["ai_response"] ?? "No answer yet"),

            const SizedBox(height: 20),

            const Text(
              "Status",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(query["status"] ?? "Unknown"),

            const SizedBox(height: 20),

            const Text(
              "Created At",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(query["created_at"] ?? "Not available"),
          ],
        ),
      ),
    );
  }
}