// import 'package:flutter/material.dart';
// import '../home_screen.dart'
//     show kPrimaryColor, kAccentColor, kResolvedColor, kAdminColor;
//
// class NotificationPage extends StatelessWidget {
//   final List<Map<String, dynamic>> notificationItems;
//   final void Function(Map<String, dynamic>) onTapNotification;
//
//   const NotificationPage({
//     super.key,
//     required this.notificationItems,
//     required this.onTapNotification,
//   });
//
//   @override
//   Widget build(BuildContext context) {
//     if (notificationItems.isEmpty) {
//       return const Center(
//         child: Column(
//           mainAxisSize: MainAxisSize.min,
//           children: [
//             Icon(Icons.notifications_none, size: 60, color: kPrimaryColor),
//             SizedBox(height: 10),
//             Text(
//               "No Notifications Yet",
//               style: TextStyle(
//                 fontSize: 22,
//                 fontWeight: FontWeight.bold,
//                 color: kPrimaryColor,
//               ),
//             ),
//             SizedBox(height: 5),
//             Text(
//               "We'll notify you here when your queries are resolved.",
//               style: TextStyle(fontSize: 16, color: Colors.grey),
//               textAlign: TextAlign.center,
//             ),
//           ],
//         ),
//       );
//     }
//
//     return ListView.builder(
//       padding: const EdgeInsets.all(10),
//       itemCount: notificationItems.length,
//       itemBuilder: (context, index) {
//         final item = notificationItems[index];
//
//         final bool isRead = item['read'] == true || item['is_read'] == true;
//         final String type = (item['type'] ?? 'general').toString();
//         final String title = (item['title'] ?? 'Notification').toString();
//
//         // CHANGE: Safe body/message conversion.
//         final String body =
//         (item['body'] ?? item['message'] ?? '').toString();
//
//         final String date =
//         (item['timestamp'] ?? item['created_at'] ?? '').toString();
//
//         Color iconColor;
//         IconData iconData;
//
//         switch (type) {
//           case 'resolved':
//           case 'query_answered':
//             iconColor = kResolvedColor;
//             iconData = Icons.check_circle_outline;
//             break;
//           case 'assigned':
//           case 'admin':
//             iconColor = kAdminColor;
//             iconData = Icons.campaign;
//             break;
//           case 'solved':
//             iconColor = kResolvedColor;
//             iconData = Icons.auto_awesome;
//             break;
//           default:
//             iconColor = Colors.grey;
//             iconData = Icons.info_outline;
//         }
//
//         return Card(
//           elevation: 2,
//           shape: RoundedRectangleBorder(
//             borderRadius: BorderRadius.circular(10),
//           ),
//           color: isRead ? Colors.white : Colors.blue.shade50,
//           margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 5),
//           child: ListTile(
//             leading: Icon(iconData, color: iconColor, size: 30),
//             title: Text(
//               title,
//               style: TextStyle(
//                 fontWeight: isRead ? FontWeight.normal : FontWeight.bold,
//                 color: kPrimaryColor,
//               ),
//             ),
//             subtitle: Text(
//               body.trim().isEmpty ? "No details available." : body,
//               maxLines: 2,
//               overflow: TextOverflow.ellipsis,
//               style: TextStyle(
//                 fontSize: 13,
//                 color: Colors.grey.shade700,
//               ),
//             ),
//             trailing: isRead
//                 ? null
//                 : const Icon(Icons.circle, color: kAccentColor, size: 10),
//             onTap: () {
//               showDialog(
//                 context: context,
//                 builder: (_) {
//                   return AlertDialog(
//                     title: Text(title),
//                     content: Column(
//                       mainAxisSize: MainAxisSize.min,
//                       crossAxisAlignment: CrossAxisAlignment.start,
//                       children: [
//                         Text(
//                           body.trim().isEmpty
//                               ? "No details available."
//                               : body,
//                           style: const TextStyle(
//                             fontSize: 15,
//                             height: 1.5,
//                           ),
//                         ),
//                         const SizedBox(height: 14),
//                         Text("Type: $type"),
//                         if (date.trim().isNotEmpty) ...[
//                           const SizedBox(height: 6),
//                           Text("Date: $date"),
//                         ],
//                       ],
//                     ),
//                     actions: [
//                       TextButton(
//                         onPressed: () => Navigator.pop(context),
//                         child: const Text("Close"),
//                       ),
//                     ],
//                   );
//                 },
//               );
//
//               onTapNotification(item);
//             },
//           ),
//         );
//       },
//     );
//   }
// }



import 'package:flutter/material.dart';
import '../home_screen.dart'
    show kPrimaryColor, kAccentColor, kResolvedColor, kAdminColor;

// CHANGE: Converted StatelessWidget → StatefulWidget to support refresh
class NotificationPage extends StatefulWidget {
  final List<Map<String, dynamic>> notificationItems;
  final void Function(Map<String, dynamic>) onTapNotification;

  // CHANGE: Added refresh callback (this will call API from parent)
  final Future<void> Function() onRefresh;

  const NotificationPage({
    super.key,
    required this.notificationItems,
    required this.onTapNotification,
    required this.onRefresh, // CHANGE
  });

  @override
  State<NotificationPage> createState() => _NotificationPageState();
}

// CHANGE: New State class added
class _NotificationPageState extends State<NotificationPage> {

  @override
  Widget build(BuildContext context) {

    // CHANGE: Wrapped entire UI inside RefreshIndicator
    return RefreshIndicator(
      onRefresh: widget.onRefresh, // calls API from parent

      child: widget.notificationItems.isEmpty
          ? ListView( // CHANGE: ListView required for pull-to-refresh
        children: const [
          SizedBox(height: 150),
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.notifications_none,
                    size: 60, color: kPrimaryColor),
                SizedBox(height: 10),
                Text(
                  "No Notifications Yet",
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    color: kPrimaryColor,
                  ),
                ),
                SizedBox(height: 5),
                Text(
                  "Pull down to refresh.",
                  style: TextStyle(fontSize: 16, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ],
      )
          : ListView.builder(
        padding: const EdgeInsets.all(10),
        itemCount: widget.notificationItems.length,
        itemBuilder: (context, index) {
          final item = widget.notificationItems[index];

          final bool isRead =
              item['read'] == true || item['is_read'] == true;
          final String type =
          (item['type'] ?? 'general').toString();
          final String title =
          (item['title'] ?? 'Notification').toString();

          final String body =
          (item['body'] ?? item['message'] ?? '').toString();

          final String date =
          (item['timestamp'] ?? item['created_at'] ?? '').toString();

          Color iconColor;
          IconData iconData;

          switch (type) {
            case 'resolved':
            case 'query_answered':
              iconColor = kResolvedColor;
              iconData = Icons.check_circle_outline;
              break;
            case 'assigned':
            case 'admin':
              iconColor = kAdminColor;
              iconData = Icons.campaign;
              break;
            case 'solved':
              iconColor = kResolvedColor;
              iconData = Icons.auto_awesome;
              break;
            default:
              iconColor = Colors.grey;
              iconData = Icons.info_outline;
          }

          return Card(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
            color: isRead ? Colors.white : Colors.blue.shade50,
            margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 5),
            child: ListTile(
              leading: Icon(iconData, color: iconColor, size: 30),
              title: Text(
                title,
                style: TextStyle(
                  fontWeight:
                  isRead ? FontWeight.normal : FontWeight.bold,
                  color: kPrimaryColor,
                ),
              ),
              subtitle: Text(
                body.trim().isEmpty
                    ? "No details available."
                    : body,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  fontSize: 13,
                  color: Colors.grey.shade700,
                ),
              ),
              trailing: isRead
                  ? null
                  : const Icon(Icons.circle,
                  color: kAccentColor, size: 10),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (_) {
                    return AlertDialog(
                      title: Text(title),
                      content: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            body.trim().isEmpty
                                ? "No details available."
                                : body,
                            style: const TextStyle(
                              fontSize: 15,
                              height: 1.5,
                            ),
                          ),
                          const SizedBox(height: 14),
                          Text("Type: $type"),
                          if (date.trim().isNotEmpty) ...[
                            const SizedBox(height: 6),
                            Text("Date: $date"),
                          ],
                        ],
                      ),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: const Text("Close"),
                        ),
                      ],
                    );
                  },
                );

                widget.onTapNotification(item);
              },
            ),
          );
        },
      ),
    );
  }
}