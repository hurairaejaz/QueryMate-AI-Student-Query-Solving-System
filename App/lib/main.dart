import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:querymate/Account%20Screens/login_screen.dart';
import 'package:querymate/Account%20Screens/signup_screen.dart';
import 'package:querymate/home_screen.dart';
import 'package:querymate/screens/landing_page.dart';
import 'package:querymate/Account%20Screens/verify_otp_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'QueryMate',
      theme: ThemeData(primarySwatch: Colors.blue),

      home: const AuthCheckScreen(),

      routes: {
        '/launch': (context) => const LandingPage(),
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignUpScreen(),
        '/home': (context) => const HomeScreen(),
        "/verify-otp": (context) => const VerifyOtpScreen(email: '',),
      },
    );
  }
}

class AuthCheckScreen extends StatefulWidget {
  const AuthCheckScreen({super.key});

  @override
  State<AuthCheckScreen> createState() => _AuthCheckScreenState();
}

class _AuthCheckScreenState extends State<AuthCheckScreen> {
  @override
  void initState() {
    super.initState();
    // ADDED: moved login check after widget build safety
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkLogin();
    });
  }

  Future<void> _checkLogin() async {
    final prefs = await SharedPreferences.getInstance();

    final isLoggedIn = prefs.getBool('is_logged_in') ?? false;
    final token = prefs.getString('access_token');

    if (!mounted) return;

    if (isLoggedIn && token != null && token.isNotEmpty) {
      Navigator.pushReplacementNamed(context, '/home');
    } else {
      Navigator.pushReplacementNamed(context, '/launch');
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: CircularProgressIndicator()),
    );
  }
}