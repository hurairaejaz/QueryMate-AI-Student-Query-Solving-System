import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import '../home_screen.dart' show kPrimaryColor, kWhatsAppGreen;

class WhatsAppPage extends StatelessWidget {
  final Widget lottie;
  final VoidCallback onWhatsAppPressed;

  const WhatsAppPage({super.key, required this.lottie, required this.onWhatsAppPressed});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            lottie,
            const SizedBox(height: 30),
            const Text(
              "Direct QueryMate Access",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: kPrimaryColor),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            const Text(
              "Chat instantly with QueryMate via WhatsApp for quick query and their response .",
              style: TextStyle(fontSize: 16, color: Colors.black54),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 60),
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(30),
                boxShadow: [BoxShadow(color: kWhatsAppGreen.withOpacity(0.5), blurRadius: 15, spreadRadius: 2, offset: const Offset(0, 5))],
              ),
              child: ElevatedButton.icon(
                onPressed: onWhatsAppPressed,
                icon: const Icon(Icons.send, color: Colors.white),
                label: const Text("Chat on WhatsApp", style: TextStyle(fontSize: 20, color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: kWhatsAppGreen,
                  minimumSize: const Size(double.infinity, 60),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                  elevation: 0,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
