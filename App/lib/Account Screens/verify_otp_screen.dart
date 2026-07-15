import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:querymate/config/app_config.dart';

const Color kPrimaryColor = Color(0xFF1C4587);

class VerifyOtpScreen extends StatefulWidget {
  final String email;

  const VerifyOtpScreen({super.key, required this.email});

  @override
  State<VerifyOtpScreen> createState() => _VerifyOtpScreenState();
}

class _VerifyOtpScreenState extends State<VerifyOtpScreen> {
  final TextEditingController _otpController = TextEditingController();

  int _seconds = 60;
  Timer? _timer;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    _seconds = 60;
    _timer?.cancel();

    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_seconds == 0) {
        timer.cancel();
      } else {
        setState(() => _seconds--);
      }
    });
  }

  Future<void> _verifyOtp() async {
    final otp = _otpController.text.trim();

    if (otp.length != 6) {
      _show("Enter valid 6-digit OTP");
      return;
    }

    setState(() => _isLoading = true);

    try {
      final res = await http.post(
        Uri.parse("${AppConfig.baseUrl}/auth/verify-signup-otp"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "email": widget.email,
          "otp": otp,
        }),
      );

      final data = jsonDecode(res.body);

      if (res.statusCode == 200) {
        _show("Verified successfully");

        Navigator.pushNamedAndRemoveUntil(
          context,
          '/',
              (route) => false,
        );
      } else {
        _show(data["detail"] ?? "Invalid OTP");
      }
    } catch (e) {
      _show("Error: $e");
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _resendOtp() async {
    try {
      await http.post(
        Uri.parse("${AppConfig.baseUrl}/auth/register"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "email": widget.email,
        }),
      );

      _show("OTP resent");
      _startTimer();
    } catch (e) {
      _show("Failed to resend OTP");
    }
  }

  void _show(String msg) {
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(msg)));
  }

  @override
  void dispose() {
    _timer?.cancel();
    _otpController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    OutlineInputBorder border(Color c, double w) => OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: c, width: w),
    );

    return Scaffold(
      backgroundColor: const Color(0xFFEAF6FF),
      body: Column(
        children: [
          Container(
            height: 200,
            width: double.infinity,
            color: kPrimaryColor,
            padding: const EdgeInsets.only(left: 30, top: 60),
            alignment: Alignment.centerLeft,
            child: const Text(
              "Verify OTP",
              style: TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold),
            ),
          ),

          const SizedBox(height: 40),

          Text("OTP sent to\n${widget.email}",
              textAlign: TextAlign.center),

          const SizedBox(height: 20),

          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 30),
            child: TextField(
              controller: _otpController,
              maxLength: 6,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: "Enter OTP",
                counterText: "",
                border: border(kPrimaryColor, 1.5),
              ),
            ),
          ),

          const SizedBox(height: 20),

          ElevatedButton(
            onPressed: _isLoading ? null : _verifyOtp,
            child: _isLoading
                ? const CircularProgressIndicator()
                : const Text("Verify"),
          ),

          const SizedBox(height: 20),

          Text(
            _seconds > 0
                ? "Resend OTP in $_seconds s"
                : "Didn’t receive OTP?",
          ),

          TextButton(
            onPressed: _seconds == 0 ? _resendOtp : null,
            child: const Text("Resend OTP"),
          ),
        ],
      ),
    );
  }
}