import 'dart:io';
import 'dart:convert';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:lottie/lottie.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:dio/dio.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'screens/history.dart';
import 'screens/whatsapp.dart';
import 'screens/notification.dart';
import 'screens/account.dart';
import 'package:querymate/config/app_config.dart';
import 'package:querymate/services/query_services.dart';
import 'package:querymate/models/query_response.dart';
import 'package:querymate/models/query_request.dart';
import 'package:querymate/services/api_services.dart';
const Color kPrimaryColor = Color(0xFF1C4587);
const Color kAccentColor = Color(0xFFF76F5E);
const Color kWhatsAppGreen = Color(0xFF25D366);
const Color kResolvedColor = Color(0xFF38A760);
const Color kAdminColor = Color(0xFFE5B80B);

class WhatsAppScreen extends StatelessWidget {
  const WhatsAppScreen({super.key});

  Future<void> _openWhatsApp(BuildContext context) async {
    const phone = "923224205957";
    final Uri uri = Uri.parse("https://wa.me/$phone");

    try {
      await launchUrl(
        uri,
        mode: LaunchMode.externalApplication,
      );
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("WhatsApp could not be opened")),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("You Can use same features on WhatsApp"),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _openWhatsApp(context),
          child: const Text("Open WhatsApp Chat"),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with WidgetsBindingObserver, TickerProviderStateMixin {
  int _currentIndex = 2;
  bool _chatStarted = false;
  bool _isSending = false;

  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;
  late Animation<int> _typewriterAnimation;
  late AnimationController _typewriterController;
  late Animation<double> _buttonGlowAnimation;

  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  final List<Map<String, dynamic>> _messages = [];
  List<Map<String, dynamic>> _historyItems = [];
  List<Map<String, dynamic>> _notificationItems = [];
  String? _activeChatId;
  String? _profileImagePath;
  String _currentEmail = '';

  static const String _welcomeText = "Welcome to QueryMate";

  String _getProfileKey(String email) {
    return 'profile_image_${email.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}';
  }

  // String get _historyKey =>
  //     'chat_history_${_currentEmail.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}';
  String get _historyKey {
    if (_currentEmail.isEmpty) {
      throw Exception("Email not loaded before accessing history key");
    }
    return 'chat_history_${_currentEmail.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}';
  }
  // Future<void> _loadNotificationsFromBackend() async {
  //   try {
  //     final res = await ApiService.getRequest(
  //       "/app/notifications",
  //       authRequired: true,
  //     );
  //
  //     if (!mounted) return;
  //
  //     setState(() {
  //       _notificationItems = List<Map<String, dynamic>>.from(
  //         res.map((x) => Map<String, dynamic>.from(x)),
  //       );
  //     });
  //   } catch (e) {
  //     debugPrint("Notification load error: $e");
  //   }
  // }

  Future<Map<String, String>> _getUserInfo() async {
    final prefs = await SharedPreferences.getInstance();

    final name = prefs.getString('name') ?? 'No name found';
    // final email = prefs.getString('email') ?? 'No email found';
    final email = prefs.getString('email');

    if (email == null || email.isEmpty) {
      debugPrint("❌ Email not found, history cannot load");
      return {};
    }

    _currentEmail = email;
    final password = prefs.getString('password') ?? 'No password found';
    final phone = prefs.getString('phone') ?? 'N/A';

    _currentEmail = email;

    return {
      "name": name,
      "email": email,
      "password": password,
      "phone": phone,
    };
  }

  // Future<void> _loadHistory() async {
  //   await _getUserInfo();
  //
  //   final prefs = await SharedPreferences.getInstance();
  //   final jsonString = prefs.getString(_historyKey);
  //
  //   // if (_currentEmail.isNotEmpty && _currentEmail != 'No email found') {
  //   //   _notificationItems = _simulatedNotifications;
  //   // }
  //
  //   if (jsonString != null && jsonString.isNotEmpty) {
  //     final List<dynamic> decodedList = json.decode(jsonString);
  //     setState(() {
  //       _historyItems =
  //           decodedList.map((item) => item as Map<String, dynamic>).toList();
  //     });
  //   } else {
  //     setState(() {
  //       _historyItems = [];
  //     });
  //   }
  // }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();

    final email = prefs.getString('email');

    if (email == null || email.isEmpty) {
      debugPrint("Cannot load history: email missing");
      setState(() => _historyItems = []);
      return;
    }

    _currentEmail = email;

    final key =
        'chat_history_${email.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}';

    final jsonString = prefs.getString(key);

    if (jsonString != null && jsonString.isNotEmpty) {
      final List<dynamic> decodedList = json.decode(jsonString);

      setState(() {
        _historyItems =
            decodedList.map((item) => Map<String, dynamic>.from(item)).toList();
      });

      debugPrint("✅ History loaded: ${_historyItems.length} items");
    } else {
      debugPrint("⚠️ No history found for this user");
      setState(() => _historyItems = []);
    }
  }

  // Future<void> _saveHistory() async {
  //   final prefs = await SharedPreferences.getInstance();
  //   final jsonString = json.encode(_historyItems);
  //   await prefs.setString(_historyKey, jsonString);
  // }

  Future<void> _saveHistory() async {
    final prefs = await SharedPreferences.getInstance();

    final email = prefs.getString('email');

    if (email == null || email.isEmpty) {
      debugPrint(" Cannot save history: email missing");
      return;
    }

    final key =
        'chat_history_${email.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}';

    final jsonString = json.encode(_historyItems);

    await prefs.setString(key, jsonString);

    debugPrint(" History saved for: $email");
  }

  Future<void> _clearSession() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('name');
    await prefs.remove('email');
    await prefs.remove('password');
    await prefs.remove('phone');

    await prefs.setBool('is_logged_in', false);
    if (!mounted) return;

    Navigator.pushNamedAndRemoveUntil(
      context,
      '/login',
          (route) => false,
    );
  }

  Future<void> _saveCurrentChatToHistory({
    required String firstQuery,
    required String botResponse,
  }) async {
    final now = DateTime.now().toIso8601String();

    _activeChatId ??= now;

    final existingIndex = _historyItems.indexWhere(
          (item) => item["chat_id"] == _activeChatId,
    );

    final chatItem = {
      "chat_id": _activeChatId,
      "title": firstQuery.length > 40
          ? "${firstQuery.substring(0, 37)}..."
          : firstQuery,
      "response_summary": botResponse.length > 50
          ? "${botResponse.substring(0, 47)}..."
          : botResponse,
      "timestamp": now,
      "full_conversation": List<Map<String, dynamic>>.from(_messages),
    };

    if (existingIndex >= 0) {
      _historyItems[existingIndex] = chatItem;
    } else {
      _historyItems.insert(0, chatItem);
    }

    await _saveHistory();
  }

  Future<void> _loadNotificationsFromBackend() async {
    try {
      final res = await ApiService.getRequest(
        "/app/notifications/",
        authRequired: true,
      );

      if (!mounted) return;

      final List items = res["items"] ?? [];
      if (items.isEmpty) {
        setState(() {
          _notificationItems = [];
        });
        return;
      }
      setState(() {
        _notificationItems = items.map((x) {
          final item = Map<String, dynamic>.from(x);

          return {
            "notification_id": item["notification_id"],
            "query_id": item["query_id"],
            "title": item["title"] ?? "Notification",
            "body": item["message"] ?? "",
            "message": item["message"] ?? "",
            "type": item["type"] ?? "general",

            // IMPORTANT FIX
            "read": item["is_read"] ?? false,
            "is_read": item["is_read"] ?? false,

            "timestamp": item["created_at"]?.toString() ?? "",
            "created_at": item["created_at"]?.toString() ?? "",
          };
        }).toList();
      });
    } catch (e) {
      debugPrint("Notification load error: $e");
    }
  }
  Future<void> _loadProfileImage() async {
    await _getUserInfo();

    if (_currentEmail.isNotEmpty && _currentEmail != 'No email found') {
      final prefs = await SharedPreferences.getInstance();
      final uniqueKey = _getProfileKey(_currentEmail);

      setState(() {
        _profileImagePath = prefs.getString(uniqueKey);
      });
    } else {
      setState(() {
        _profileImagePath = null;
      });
    }
  }

  Future<void> _pickProfileImage() async {
    if (_currentEmail.isEmpty || _currentEmail == 'No email found') {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Cannot set profile image. User data missing."),
        ),
      );
      return;
    }

    final picker = ImagePicker();
    final XFile? file = await picker.pickImage(source: ImageSource.gallery);

    if (file != null) {
      try {
        final appDir = await getApplicationDocumentsDirectory();
        final fileName = path.basename(file.path);
        final localPath = '${appDir.path}/$fileName';
        final newImage = await File(file.path).copy(localPath);

        final prefs = await SharedPreferences.getInstance();
        final uniqueKey = _getProfileKey(_currentEmail);

        await prefs.setString(uniqueKey, newImage.path);

        setState(() {
          _profileImagePath = newImage.path;
        });
      } catch (e) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Failed to save profile image.")),
        );
      }
    }
  }

  // void _deleteAccount() async {
  //   final bool? confirm = await showDialog<bool>(
  //     context: context,
  //     builder: (context) => AlertDialog(
  //       title: const Text("Permanently Delete Account? 🗑️"),
  //       content: const Text(
  //         "Are you sure you want to delete your QueryMate account? This action cannot be undone.",
  //       ),
  //       actions: [
  //         TextButton(
  //           onPressed: () => Navigator.of(context).pop(false),
  //           child: const Text("Cancel"),
  //         ),
  //         ElevatedButton(
  //           onPressed: () => Navigator.of(context).pop(true),
  //           style: ElevatedButton.styleFrom(backgroundColor: kAccentColor),
  //           child: const Text(
  //             "Delete",
  //             style: TextStyle(color: Colors.white),
  //           ),
  //         ),
  //       ],
  //     ),
  //   );
  //
  //   if (confirm != true) return;
  //
  //   try {
  //     final prefs = await SharedPreferences.getInstance();
  //     final token = prefs.getString("access_token");
  //     print("Using token: $token");
  //     // 🔥 STEP 1: DELETE FROM BACKEND (IMPORTANT FIX)
  //     final response = await http.delete(
  //       Uri.parse("${AppConfig.baseUrl}/user/delete-account"),
  //       headers: {
  //         "Authorization": "Bearer $token",
  //         "Accept": "application/json",
  //       },
  //     );
  //     print("Delete Status: ${response.statusCode}");
  //     print("Delete Body: ${response.body}");
  //
  //     if (response.statusCode != 200 && response.statusCode != 204) {
  //       if (mounted) {
  //         ScaffoldMessenger.of(context).showSnackBar(
  //           const SnackBar(content: Text("Failed to delete account on server")),
  //         );
  //       }
  //       return;
  //     }
  //
  //     // 🔥 STEP 2: CLEAR PROFILE IMAGE
  //     if (_currentEmail.isNotEmpty && _currentEmail != 'No email found') {
  //       final uniqueKey = _getProfileKey(_currentEmail);
  //       await prefs.remove(uniqueKey);
  //     }
  //
  //     // 🔥 STEP 3: CLEAR ALL LOCAL DATA
  //     await prefs.remove('reg_name');
  //     await prefs.remove('reg_email');
  //     await prefs.remove('reg_password');
  //     await prefs.remove('reg_phone');
  //
  //     await prefs.remove(_historyKey);
  //
  //     await prefs.remove('name');
  //     await prefs.remove('email');
  //     await prefs.remove('password');
  //     await prefs.remove('phone');
  //
  //     await prefs.remove("access_token");
  //     await prefs.setBool('is_logged_in', false);
  //
  //     // 🔥 STEP 4: GO TO LOGIN SCREEN
  //     if (mounted) {
  //       Navigator.pushNamedAndRemoveUntil(
  //         context,
  //         '/login',
  //             (route) => false,
  //       );
  //     }
  //   } catch (e) {
  //     if (mounted) {
  //       ScaffoldMessenger.of(context).showSnackBar(
  //         SnackBar(content: Text("Error deleting account: $e")),
  //       );
  //     }
  //   }
  // }

  void _deleteAccount() async {
    final bool? confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Delete Account?"),
        content: const Text(
          "This action cannot be undone.",
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(context, true),
            child: const Text("Delete"),
          ),
        ],
      ),
    );

    if (confirm != true) return;

    try {
      final prefs = await SharedPreferences.getInstance();

      // ❌ skip backend call completely

      // 🔥 CLEAR EVERYTHING LOCAL
      await prefs.clear();

      if (!mounted) return;

      // 🔥 GO TO LOGIN
      Navigator.pushNamedAndRemoveUntil(
        context,
        '/login',
            (route) => false,
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
  }

  Future<void> _openAnyLink(String url) async {
    if (url.trim().isEmpty) return;

    final Uri uri = Uri.parse(url);

    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Could not open link")),
      );
    }
  }
  Future<void> _downloadAndOpenDocument({
    required String url,
    required String fileName,
  }) async {
    try {
      if (!url.startsWith("http")) {
        url = "${AppConfig.baseUrl}$url";
      }

      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString("access_token");

      final dir = await getApplicationDocumentsDirectory();
      final savePath = p.join(dir.path, fileName);

      await Dio().download(
        url,
        savePath,
        options: Options(
          headers: {
            "Accept": "application/octet-stream",
            if (token != null && token.isNotEmpty)
              "Authorization": "Bearer $token",
          },
        ),
      );

      final result = await OpenFilex.open(savePath);

      if (result.type != ResultType.done && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Could not open file: ${result.message}")),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to download/open document: $e")),
      );
    }
  }


  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage() async {
    if (_controller.text.trim().isEmpty || _isSending) return;

    final userQuery = _controller.text.trim();

    setState(() {
      _chatStarted = true;
      _isSending = true;

      _messages.add({
        "role": "user",
        "type": "text",
        "text": userQuery,
      });

      _messages.add({
        "role": "bot",
        "type": "typing",
      });

      _controller.clear();
    });

    _scrollToBottom();

    try {
      final request = QueryRequest(queryText: userQuery);
      final QueryResponse response = await QueryService.submitQuery(request);

      String botResponse;
      if (response.status == "answered" &&
          response.answer != null &&
          response.answer!.trim().isNotEmpty) {
        botResponse = response.answer!;
      } else if (response.status == "escalated") {
        botResponse =
        "Unfortunately our system could not find relevant answers about your query  in the department knowledge base. Your query has been forwarded to admin.Soon you will get the response. Thanks for your Patience ❤️";
      } else {
        botResponse = "Sorry, I could not understand your query.";
      }

      String? documentName;
      String? documentUrl;

      final documents = response.documents;

      if (documents.isNotEmpty) {
        final documentData = documents.first;

        documentName = (documentData["file_name"] ?? "document").toString();

        documentUrl = (documentData["download_url"] ??
            documentData["open_url"] ??
            documentData["file_url"])
            ?.toString();

        if (documentUrl != null && documentUrl.trim().isNotEmpty) {
          if (!documentUrl.startsWith("http")) {
            documentUrl = "${AppConfig.baseUrl}$documentUrl";
          }
        }
      }

      setState(() {
        _messages.removeWhere((msg) => msg["type"] == "typing");

        _messages.add({
          "role": "bot",
          "type": "combined",
          "text": botResponse,
          "file_name": documentName,
          "file_url": documentUrl,
        });
      });

      await _saveCurrentChatToHistory(
        firstQuery: _messages.firstWhere(
              (msg) => msg["role"] == "user",
          orElse: () => {"text": userQuery},
        )["text"].toString(),
        botResponse: botResponse,
      );
      await _loadHistory();
      // await _saveHistory();
      _scrollToBottom();
    } catch (e) {
      setState(() {
        _messages.removeWhere((msg) => msg["type"] == "typing");

        _messages.add({
          "role": "bot",
          "type": "combined",
          "text": "Error: $e",
          "file_name": null,
          "file_url": null,
        });
      });

      _scrollToBottom();
    } finally {
      setState(() {
        _isSending = false;
      });
    }
  }

  Future<bool> _onWillPop() async {
    if (_currentIndex != 2) {
      setState(() => _currentIndex = 2);
      return false;
    }
    return true;
  }

  @override
  void initState() {
    super.initState();
    _loadProfileImage();
    // _loadHistory();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadHistory();
    });
    WidgetsBinding.instance.addObserver(this);

    // _loadNotificationsFromBackend();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadNotificationsFromBackend();
    });
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true);

    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.15).animate(
      CurvedAnimation(
        parent: _animationController,
        curve: Curves.easeInQuad,
      ),
    );

    _buttonGlowAnimation = Tween<double>(begin: 0.0, end: 10.0).animate(
      CurvedAnimation(
        parent: _animationController,
        curve: Curves.easeOut,
      ),
    );

    _typewriterController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat();

    _typewriterAnimation = IntTween(
      begin: 0,
      end: _welcomeText.length,
    ).animate(
      CurvedAnimation(
        parent: _typewriterController,
        curve: const Interval(0.0, 0.9, curve: Curves.linear),
      ),
    );
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _loadNotificationsFromBackend();
      _loadHistory();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _animationController.dispose();
    _typewriterController.dispose();
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bool showDefaultAppBar = _currentIndex != 4;

    final List<Widget> pages = [
      HistoryPage(
        historyItems: _historyItems,
        onGoToChat: () => setState(() => _currentIndex = 2),
        onTapHistory: (item) {
          setState(() {
            _messages.clear();

            final conversation = item["full_conversation"];

            if (conversation is List) {
              _messages.addAll(
                conversation.map((x) => Map<String, dynamic>.from(x)).toList(),
              );
            } else {
              _messages.add({
                "role": "user",
                "type": "text",
                "text": item["query"] ?? "",
              });

              _messages.add({
                "role": "bot",
                "type": "combined",
                "text": item["response_summary"] ?? "",
                "file_name": null,
                "file_url": null,
              });
            }

            _activeChatId = item["chat_id"]?.toString();
            _chatStarted = true;
            _currentIndex = 2;
          });

          _scrollToBottom();
        },
      ),
      WhatsAppPage(
        lottie: Lottie.asset('assets/logo.json', height: 250, repeat: true),
        onWhatsAppPressed: () async {
          final Uri uri = Uri.parse("https://wa.me/923224205957");
          if (await canLaunchUrl(uri)) {
            await launchUrl(uri, mode: LaunchMode.externalApplication);
          } else {
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Could not open WhatsApp")),
              );
            }
          }
        },
      ),
      _chatStarted ? _buildChatUI() : _buildWelcomeUI(),
      NotificationPage(
        notificationItems: _notificationItems,
        onTapNotification: (item) {
          setState(() {
            item["read"] = true;
            item["is_read"] = true;
          });
        },
       onRefresh: () async {
          await _loadNotificationsFromBackend();
        },
      ),
      AccountPage(
        getUserInfo: _getUserInfo,
        profileImagePath: _profileImagePath,
        pickProfileImage: _pickProfileImage,
        clearSession: _clearSession,
        deleteAccount: _deleteAccount,
      ),
    ];

    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        backgroundColor: const Color(0xFFF7F8FA),
        appBar: showDefaultAppBar
            ? AppBar(
          title: const Text(
            "QueryMate",
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          backgroundColor: kPrimaryColor,
          leading: _currentIndex == 2
              ? null
              : IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.white),
            onPressed: () {
              setState(() => _currentIndex = 2);
            },
          ),
          centerTitle: true,
        )
            : null,
        body: SafeArea(child: pages[_currentIndex]),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          type: BottomNavigationBarType.fixed,
          backgroundColor: Colors.white,
          selectedItemColor: kPrimaryColor,
          unselectedItemColor: Colors.grey.shade600,
          onTap: (index) {
            setState(() {
              _currentIndex = index;
            });

            if (index == 0) {
              _loadHistory();
            }

            if (index == 3) {
              _loadNotificationsFromBackend();
            }
          },
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.history),
              label: "History",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.grid_view),
              label: "WhatsApp",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.chat, size: 32),
              label: "Chat",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.notifications),
              label: "Notification",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              label: "Account",
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChatUI() {
    return LayoutBuilder(
      builder: (context, constraints) {
        final bool isSmallScreen = constraints.maxWidth < 600;

        return Column(
          children: [
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: EdgeInsets.symmetric(
                  horizontal: isSmallScreen ? 10 : 18,
                  vertical: 14,
                ),
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final msg = _messages[index];
                  return _buildMessageBubble(msg, constraints.maxWidth);
                },
              ),
            ),
            _buildInputArea(isSmallScreen),
          ],
        );
      },
    );
  }

  Widget _buildMessageBubble(Map<String, dynamic> msg, double screenWidth) {
    final bool isUser = msg["role"] == "user";
    final bool isTyping = msg["type"] == "typing";

    final double maxBubbleWidth = screenWidth > 700
        ? screenWidth * 0.65
        : screenWidth * 0.82;

    if (isTyping) {
      return Align(
        alignment: Alignment.centerLeft,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 6),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(18),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.06),
                blurRadius: 8,
                offset: const Offset(0, 3),
              )
            ],
          ),
          child: const Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              _TypingDot(),
              SizedBox(width: 5),
              _TypingDot(),
              SizedBox(width: 5),
              _TypingDot(),
            ],
          ),
        ),
      );
    }

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxWidth: maxBubbleWidth,
          minWidth: 90,
        ),
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 6),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: isUser ? kPrimaryColor : Colors.white,
            borderRadius: BorderRadius.only(
              topLeft: const Radius.circular(18),
              topRight: const Radius.circular(18),
              bottomLeft:
              isUser ? const Radius.circular(18) : const Radius.circular(6),
              bottomRight:
              isUser ? const Radius.circular(6) : const Radius.circular(18),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.06),
                blurRadius: 8,
                offset: const Offset(0, 3),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if ((msg["text"] ?? "").toString().trim().isNotEmpty)
                _buildMessageText(
                  text: msg["text"].toString(),
                  isUser: isUser,
                ),
              if (!isUser &&
                  (msg["file_url"] ?? "").toString().trim().isNotEmpty) ...[
                const SizedBox(height: 12),
                InkWell(
                  onTap: () => _downloadAndOpenDocument(
                    url: msg["file_url"].toString(),
                    fileName: (msg["file_name"] ?? "document.pdf").toString(),
                  ),
                  borderRadius: BorderRadius.circular(12),
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF3F7FD),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFFD5E3F4)),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.attach_file, color: kPrimaryColor),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            (msg["file_name"] ?? "Open document").toString(),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                              fontWeight: FontWeight.w600,
                              color: kPrimaryColor,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        const Icon(Icons.open_in_new, color: kPrimaryColor),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMessageText({
    required String text,
    required bool isUser,
  }) {
    final urlRegex = RegExp(r'(https?:\/\/[^\s]+)');
    final matches = urlRegex.allMatches(text);

    if (matches.isEmpty) {
      return Text(
        text,
        style: TextStyle(
          fontSize: 15.5,
          height: 1.45,
          color: isUser ? Colors.white : Colors.black87,
        ),
      );
    }

    final List<TextSpan> spans = [];
    int start = 0;

    for (final match in matches) {
      if (match.start > start) {
        spans.add(
          TextSpan(
            text: text.substring(start, match.start),
            style: TextStyle(
              fontSize: 15.5,
              height: 1.45,
              color: isUser ? Colors.white : Colors.black87,
            ),
          ),
        );
      }

      final url = match.group(0)!;
      spans.add(
        TextSpan(
          text: url,
          style: TextStyle(
            fontSize: 15.5,
            height: 1.45,
            color: isUser ? Colors.white70 : Colors.blue,
            decoration: TextDecoration.underline,
          ),
          recognizer: TapGestureRecognizer()
            ..onTap = () {
              _openAnyLink(url);
            },
        ),
      );

      start = match.end;
    }

    if (start < text.length) {
      spans.add(
        TextSpan(
          text: text.substring(start),
          style: TextStyle(
            fontSize: 15.5,
            height: 1.45,
            color: isUser ? Colors.white : Colors.black87,
          ),
        ),
      );
    }

    return RichText(
      text: TextSpan(children: spans),
    );
  }

  Widget _buildInputArea(bool isSmallScreen) {
    return Container(
      padding: EdgeInsets.fromLTRB(
        isSmallScreen ? 10 : 16,
        8,
        isSmallScreen ? 10 : 16,
        12,
      ),
      decoration: const BoxDecoration(
        color: Colors.transparent,
      ),
      child: SafeArea(
        top: false,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(18.0),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.08),
                blurRadius: 12,
                offset: const Offset(0, 4),
              )
            ],
            border: Border.all(color: Colors.grey.shade300, width: 1),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Expanded(
                child: TextField(
                  controller: _controller,
                  minLines: 1,
                  maxLines: 4,
                  textInputAction: TextInputAction.send,
                  decoration: const InputDecoration(
                    hintText: "Type your query...",
                    border: InputBorder.none,
                    contentPadding:
                    EdgeInsets.symmetric(horizontal: 8, vertical: 10),
                  ),
                  onSubmitted: (_) => _sendMessage(),
                ),
              ),
              const SizedBox(width: 8),
              Material(
                color: kPrimaryColor,
                borderRadius: BorderRadius.circular(14),
                child: InkWell(
                  borderRadius: BorderRadius.circular(14),
                  onTap: _isSending ? null : _sendMessage,
                  child: Container(
                    width: 48,
                    height: 48,
                    alignment: Alignment.center,
                    child: _isSending
                        ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2.2,
                        color: Colors.white,
                      ),
                    )
                        : const Icon(
                      Icons.send_rounded,
                      color: Colors.white,
                      size: 22,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeUI() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 22),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedBuilder(
              animation: _scaleAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _scaleAnimation.value,
                  child: child,
                );
              },
              child: Container(
                width: 160,
                height: 160,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.white.withOpacity(0.08),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.2),
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 20,
                      spreadRadius: 5,
                    )
                  ],
                ),
                child: Center(
                  child: ClipOval(
                    child: Image.asset(
                      'assets/app_icon.png',
                      height: 110,
                      width: 110,
                      fit: BoxFit.contain,
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 10),
            AnimatedBuilder(
              animation: _typewriterAnimation,
              builder: (context, child) {
                final text =
                _welcomeText.substring(0, _typewriterAnimation.value);
                return Text(
                  text,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: kPrimaryColor,
                  ),
                );
              },
            ),
            const SizedBox(height: 25),
            AnimatedBuilder(
              animation: _buttonGlowAnimation,
              builder: (context, child) {
                return Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: [
                      BoxShadow(
                        color: kPrimaryColor.withOpacity(0.4),
                        blurRadius: _buttonGlowAnimation.value,
                        spreadRadius: _buttonGlowAnimation.value / 2,
                      ),
                    ],
                  ),
                  child: ElevatedButton(
                    onPressed: () {
                      _animationController.stop();
                      _typewriterController.stop();

                      setState(() {
                        _messages.clear();
                        _activeChatId = DateTime.now().toIso8601String();
                        _chatStarted = true;
                      });
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: kPrimaryColor,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 30,
                        vertical: 14,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      elevation: 0,
                      shadowColor: Colors.transparent,
                    ),
                    child: const Text(
                      "Start a Chat",
                      style: TextStyle(fontSize: 18, color: Colors.white),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _TypingDot extends StatefulWidget {
  const _TypingDot();

  @override
  State<_TypingDot> createState() => _TypingDotState();
}

class _TypingDotState extends State<_TypingDot>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 700),
    )..repeat(reverse: true);

    _opacity = Tween<double>(begin: 0.3, end: 1).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _opacity,
      child: Container(
        width: 8,
        height: 8,
        decoration: BoxDecoration(
          color: kPrimaryColor,
          borderRadius: BorderRadius.circular(10),
        ),
      ),
    );
  }
}