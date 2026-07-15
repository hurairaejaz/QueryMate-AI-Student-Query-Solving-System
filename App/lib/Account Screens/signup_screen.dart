import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:querymate/config/app_config.dart';

const Color kPrimaryColor = Color(0xFF1C4587);

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();

  String? _passwordError;
  String? _confirmPasswordError;
  bool _isLoading = false;
  bool _showUogWarning = false;

  @override
  void initState() {
    super.initState();
    // Listen to email changes to show the UOG warning
    _emailController.addListener(() {
      setState(() {
        _showUogWarning = _emailController.text.trim().toLowerCase().endsWith('@uog.edu.pk');
      });
    });
  }

  void _validatePasswords() {
    final password = _passwordController.text.trim();
    final confirm = _confirmPasswordController.text.trim();

    setState(() {
      if (password.length < 6) {
        _passwordError = 'Password must be at least 6 characters long';
      } else {
        _passwordError = null;
      }

      if (password != confirm) {
        _confirmPasswordError = 'Passwords do not match';
      } else {
        _confirmPasswordError = null;
      }
    });
  }

  // Future<void> _signUp() async {
  //   _validatePasswords();
  //   if (_passwordError != null || _confirmPasswordError != null) return;
  //
  //   final name = _nameController.text.trim();
  //   final phone = _phoneController.text.trim();
  //   final email = _emailController.text.trim().toLowerCase();
  //   final password = _passwordController.text.trim();
  //
  //   if (name.isEmpty || phone.isEmpty || email.isEmpty || password.isEmpty) {
  //     ScaffoldMessenger.of(context).showSnackBar(
  //       const SnackBar(content: Text("All fields are required")),
  //     );
  //     return;
  //   }
  //
  //   setState(() => _isLoading = true);
  //
  //   try {
  //     final response = await http.post(
  //       Uri.parse("${AppConfig.baseUrl}/auth/register"),
  //       headers: {"Content-Type": "application/json"},
  //       body: jsonEncode({
  //         "full_name": name,
  //         "phone": phone,
  //         "email": email,
  //         "password": password,
  //       }),
  //     );
  //
  //     final data = jsonDecode(response.body);
  //
  //     if (response.statusCode >= 200 || response.statusCode < 300) {
  //       if (!mounted) return;
  //       ScaffoldMessenger.of(context).showSnackBar(
  //         const SnackBar(content: Text("Account created successfully")),
  //       );
  //       Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
  //     } else {
  //       final error = data["detail"] ?? "Signup failed";
  //       ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error)));
  //     }
  //   } catch (e) {
  //     ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
  //   } finally {
  //     if (mounted) setState(() => _isLoading = false);
  //   }
  // }

  Future<void> _signUp() async {
    _validatePasswords();
    if (_passwordError != null || _confirmPasswordError != null) return;

    final name = _nameController.text.trim();
    final phone = _phoneController.text.trim();
    final email = _emailController.text.trim().toLowerCase();
    final password = _passwordController.text.trim();

    if (name.isEmpty || phone.isEmpty || email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("All fields are required")),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final response = await http.post(
        Uri.parse("${AppConfig.baseUrl}/auth/register"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "full_name": name,
          "phone": phone,
          "email": email,
          "password": password,
        }),
      );

      final data = jsonDecode(response.body);

      // ✅ Handle ALL success status codes properly
      if (response.statusCode >= 200 && response.statusCode < 300) {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Account created successfully")),
        );

        // ✅ Small delay for smooth UX
        Future.delayed(const Duration(milliseconds: 500), () {
          Navigator.pushReplacementNamed(
            context,
            '/login',
            arguments: email, // optional (for autofill)
          );
        });

      } else {
        final error = data["detail"] ?? "Signup failed";
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error)),
        );
      }

    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFEAF6FF),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header
            Container(
              height: 220,
              width: double.infinity,
              decoration: const BoxDecoration(
                color: kPrimaryColor,
                borderRadius: BorderRadius.only(bottomLeft: Radius.circular(100)),
              ),
              alignment: Alignment.centerLeft,
              padding: const EdgeInsets.only(left: 30, top: 60),
              child: const Text(
                "Create\nYour Account",
                style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 30),

            // Input Fields
            _buildField(_nameController, "Full Name", Icons.person_outline),
            _buildField(_phoneController, "Phone Number", Icons.phone_outlined),
            _buildField(_emailController, "Email", Icons.email_outlined),

            // UOG Email Warning Note
            if (_showUogWarning)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 35, vertical: 5),
                child: const Text(
                  "Note: Remember your password carefully. Resetting passwords for university emails can be difficult.",
                  style: TextStyle(color: Colors.redAccent, fontSize: 12, fontWeight: FontWeight.w500),
                ),
              ),

            _buildField(_passwordController, "Password", Icons.lock_outline, isPassword: true),
            _buildField(_confirmPasswordController, "Confirm Password", Icons.lock_outline, isPassword: true),

            const SizedBox(height: 30),

            // Create Account Button
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30),
              child: ElevatedButton(
                onPressed: _isLoading ? null : _signUp,
                style: ElevatedButton.styleFrom(
                  backgroundColor: kPrimaryColor,
                  minimumSize: const Size(double.infinity, 55),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("Create Account", style: TextStyle(color: Colors.white, fontSize: 18)),
              ),
            ),

            const SizedBox(height: 20),

            // Login Link
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text("Already have an account? ", style: TextStyle(color: Colors.black54)),
                GestureDetector(
                  onTap: () => Navigator.pushReplacementNamed(context, '/login'),
                  child: const Text(
                    "Login",
                    style: TextStyle(color: kPrimaryColor, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildField(TextEditingController controller, String label, IconData icon, {bool isPassword = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 8),
      child: TextField(
        controller: controller,
        obscureText: isPassword,
        onChanged: isPassword ? (_) => _validatePasswords() : null,
        decoration: InputDecoration(
          labelText: label,
          filled: true,
          fillColor: Colors.white.withOpacity(0.5),
          errorText: label == "Password" ? _passwordError : (label == "Confirm Password" ? _confirmPasswordError : null),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Colors.black45)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Colors.black45)),
          prefixIcon: Icon(icon, color: kPrimaryColor),
        ),
      ),
    );
  }
}