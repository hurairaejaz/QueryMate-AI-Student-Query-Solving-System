import 'package:flutter/material.dart';
import '../home_screen.dart' show kPrimaryColor;

class HistoryPage extends StatelessWidget {
  final List<Map<String, dynamic>> historyItems;
  final VoidCallback onGoToChat;

  // CHANGE: Added callback to open selected history chat.
  final void Function(Map<String, dynamic>) onTapHistory;

  const HistoryPage({
    super.key,
    required this.historyItems,
    required this.onGoToChat,

    // CHANGE: Added required parameter.
    required this.onTapHistory,
  });

  @override
  Widget build(BuildContext context) {
    if (historyItems.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.history, size: 60, color: kPrimaryColor),
            const SizedBox(height: 10),
            const Text(
              "No History Found",
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: kPrimaryColor,
              ),
            ),
            const SizedBox(height: 5),
            const Text(
              "Start a new chat to save your first query.",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: onGoToChat,
              style: ElevatedButton.styleFrom(
                backgroundColor: kPrimaryColor,
                padding:
                const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text(
                "Go to Chat",
                style: TextStyle(fontSize: 16, color: Colors.white),
              ),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(10),
      itemCount: historyItems.length,
      itemBuilder: (context, index) {
        final item = historyItems[index];

        String? getFirstUserMessage(Map<String, dynamic> item) {
          final conversation = item["full_conversation"];

          if (conversation is List) {
            for (final msg in conversation) {
              if (msg is Map && msg["role"] == "user") {
                final text = msg["text"]?.toString().trim();
                if (text != null && text.isNotEmpty) {
                  return text.length > 40 ? "${text.substring(0, 37)}..." : text;
                }
              }
            }
          }

          return null;
        }

        final query = (item['title'] ??
            item['query'] ??
            getFirstUserMessage(item) ??
            'Untitled Chat')
            .toString();
        final summary = (item['response_summary'] ?? '').toString();

        // CHANGE: Safe timestamp parsing.
        final rawTimestamp = item['timestamp']?.toString();
        final timestamp = DateTime.tryParse(rawTimestamp ?? '');

        final timeText = timestamp == null
            ? ''
            : "${timestamp.hour}:${timestamp.minute.toString().padLeft(2, '0')}";

        return Card(
          elevation: 4,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 5),
          child: ListTile(
            leading: const Icon(Icons.forum, color: kPrimaryColor),
            title: Text(
              query,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: kPrimaryColor,
              ),
            ),
            subtitle: Text(
              summary,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(color: Colors.grey.shade600),
            ),
            trailing: Text(
              timeText,
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),

            // CHANGE: Open selected conversation instead of only showing snackbar.
            onTap: () => onTapHistory(item),
          ),
        );
      },
    );
  }
}
