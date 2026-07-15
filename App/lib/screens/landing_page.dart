// import 'package:flutter/material.dart';
//
// // Brand Constants
// const Color kPrimaryColor = Color(0xFF1C4587);
// const Color kDeepBlue = Color(0xFF0D2D5E);
//
// class LandingPage extends StatelessWidget {
//   const LandingPage({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Stack(
//         children: [
//           // 1. Background Gradient
//           Container(
//             decoration: const BoxDecoration(
//               gradient: LinearGradient(
//                 begin: Alignment.topLeft,
//                 end: Alignment.bottomRight,
//                 colors: [kPrimaryColor, kDeepBlue],
//               ),
//             ),
//           ),
//
//           // 2. Main Content
//           SafeArea(
//             child: Padding(
//               padding: const EdgeInsets.symmetric(horizontal: 32),
//               child: Column(
//                 children: [
//                   const Spacer(flex: 3),
//
//                   // Circle Logo with "Glow"
//                   Container(
//                     width: 160,
//                     height: 160,
//                     decoration: BoxDecoration(
//                       shape: BoxShape.circle,
//                       color: Colors.white.withOpacity(0.08),
//                       border: Border.all(
//                         color: Colors.white.withOpacity(0.2),
//                         width: 2,
//                       ),
//                       boxShadow: [
//                         BoxShadow(
//                           color: Colors.black.withOpacity(0.1),
//                           blurRadius: 20,
//                           spreadRadius: 5,
//                         )
//                       ],
//                     ),
//                     child: Center(
//                       child: ClipOval(
//                         child: Image.asset(
//                           'assets/app_icon.png',
//                           height: 110,
//                           width: 110,
//                           fit: BoxFit.contain,
//                         ),
//                       ),
//                     ),
//                   ),
//
//                   const SizedBox(height: 40),
//
//                   // Introduction Header
//                   const Text(
//                     "QueryMate",
//                     style: TextStyle(
//                       fontSize: 42,
//                       fontWeight: FontWeight.w800,
//                       color: Colors.white,
//                       letterSpacing: 1.5,
//                     ),
//                   ),
//
//                   const SizedBox(height: 16),
//
//                   // Short Introduction Subtext
//                   Text(
//                     "Instant answers for your academic and department queries. Powered by Artificial Intelligence.",
//                     textAlign: TextAlign.center,
//                     style: TextStyle(
//                       color: Colors.white.withOpacity(0.85),
//                       fontSize: 16,
//                       height: 1.6,
//                       fontWeight: FontWeight.w300,
//                     ),
//                   ),
//
//                   const Spacer(flex: 3),
//
//                   // Action Buttons
//                   _buildActionButtons(context),
//
//                   const Spacer(flex: 1),
//
//                   // Decent Footer
//                   _buildFooter(),
//
//                   const SizedBox(height: 20),
//                 ],
//               ),
//             ),
//           ),
//         ],
//       ),
//     );
//   }
//
//   Widget _buildActionButtons(BuildContext context) {
//     return Column(
//       children: [
//         // Primary Action: Login
//         SizedBox(
//           width: double.infinity,
//           height: 58,
//           child: ElevatedButton(
//             onPressed: () => Navigator.pushNamed(context, '/login'),
//             style: ElevatedButton.styleFrom(
//               backgroundColor: Colors.white,
//               foregroundColor: kPrimaryColor,
//               elevation: 0,
//               shape: RoundedRectangleBorder(
//                 borderRadius: BorderRadius.circular(18),
//               ),
//             ),
//             child: const Text(
//               "Login",
//               style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
//             ),
//           ),
//         ),
//
//         const SizedBox(height: 16),
//
//         // Secondary Action: Signup
//         SizedBox(
//           width: double.infinity,
//           height: 58,
//           child: OutlinedButton(
//             onPressed: () => Navigator.pushNamed(context, '/signup'),
//             style: OutlinedButton.styleFrom(
//               side: const BorderSide(color: Colors.white60, width: 1.5),
//               shape: RoundedRectangleBorder(
//                 borderRadius: BorderRadius.circular(18),
//               ),
//             ),
//             child: const Text(
//               "Create Account",
//               style: TextStyle(
//                   fontSize: 18,
//                   color: Colors.white,
//                   fontWeight: FontWeight.w500
//               ),
//             ),
//           ),
//         ),
//       ],
//     );
//   }
//
//   Widget _buildFooter() {
//     return Column(
//       children: [
//         Container(
//           width: 40,
//           height: 2,
//           color: Colors.white24,
//         ),
//         const SizedBox(height: 12),
//         const Text(
//           "Developed By Huraira Ejaz , Ali Raza, Syed Ali Wali Haider Naqvi ",
//           style: TextStyle(
//             color: Colors.white38,
//             fontSize: 10,
//             fontWeight: FontWeight.bold,
//             letterSpacing: 2.0,
//           ),
//         ),
//       ],
//     );
//   }
// }

import 'package:flutter/material.dart';

const Color kPrimaryColor = Color(0xFF1C4587);
const Color kAccentBlue = Color(0xFF4F8CFF);

class LandingPage extends StatefulWidget {
  const LandingPage({super.key});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1100),
    );

    _fadeAnimation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOut,
    );

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.18),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
    );

    _scaleAnimation = Tween<double>(
      begin: 0.82,
      end: 1.0,
    ).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Widget _animatedChild(Widget child) {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: SlideTransition(
        position: _slideAnimation,
        child: child,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0B1F45),
              kPrimaryColor,
              Color(0xFF071A36),
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 26),
            child: Column(
              children: [
                const SizedBox(height: 28),

                Align(
                  alignment: Alignment.topRight,
                  child: _animatedChild(
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 8,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(30),
                        border: Border.all(color: Colors.white24),
                      ),
                      child: const Text(
                        "AI Powered",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                ),

                const Spacer(),

                ScaleTransition(
                  scale: _scaleAnimation,
                  child: Container(
                    width: 178,
                    height: 178,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        colors: [
                          Colors.white.withOpacity(0.22),
                          Colors.white.withOpacity(0.06),
                        ],
                      ),
                      border: Border.all(
                        color: Colors.white.withOpacity(0.25),
                        width: 2,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: kAccentBlue.withOpacity(0.35),
                          blurRadius: 45,
                          spreadRadius: 6,
                        ),
                      ],
                    ),
                    child: Center(
                      child: Container(
                        width: 130,
                        height: 130,
                        decoration: const BoxDecoration(
                          shape: BoxShape.circle,
                          color: Colors.white,
                        ),
                        child: ClipOval(
                          child: Padding(
                            padding: const EdgeInsets.all(14),
                            child: Image.asset(
                              'assets/app_icon.png',
                              fit: BoxFit.contain,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 34),

                _animatedChild(
                  const Text(
                    "QueryMate",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 44,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                      letterSpacing: 1.2,
                    ),
                  ),
                ),

                const SizedBox(height: 14),

                _animatedChild(
                  Text(
                    "Ask academic, department, and support queries instantly with a smart AI assistant.",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.82),
                      fontSize: 16,
                      height: 1.5,
                      fontWeight: FontWeight.w400,
                    ),
                  ),
                ),

                const SizedBox(height: 28),

                _animatedChild(
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _featureChip(Icons.flash_on_rounded, "Fast"),
                      const SizedBox(width: 10),
                      _featureChip(Icons.school_rounded, "Academic"),
                      const SizedBox(width: 10),
                      _featureChip(Icons.support_agent_rounded, "Support"),
                    ],
                  ),
                ),

                const Spacer(),

                _animatedChild(_buildActionButtons(context)),

                const SizedBox(height: 24),

                _animatedChild(_buildFooter()),

                const SizedBox(height: 18),
              ],
            ),
          ),
        ),
      ),
    );
  }

  static Widget _featureChip(IconData icon, String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.11),
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: Colors.white.withOpacity(0.16)),
      ),
      child: Row(
        children: [
          Icon(icon, size: 15, color: Colors.white),
          const SizedBox(width: 6),
          Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButtons(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          height: 58,
          child: ElevatedButton(
            onPressed: () => Navigator.pushNamed(context, '/login'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: kPrimaryColor,
              elevation: 8,
              shadowColor: Colors.black26,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18),
              ),
            ),
            child: const Text(
              "Login",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
        ),
        const SizedBox(height: 14),
        SizedBox(
          width: double.infinity,
          height: 58,
          child: OutlinedButton(
            onPressed: () => Navigator.pushNamed(context, '/signup'),
            style: OutlinedButton.styleFrom(
              side: BorderSide(
                color: Colors.white.withOpacity(0.55),
                width: 1.4,
              ),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18),
              ),
              backgroundColor: Colors.white.withOpacity(0.08),
            ),
            child: const Text(
              "Create Account",
              style: TextStyle(
                fontSize: 17,
                color: Colors.white,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFooter() {
    return Column(
      children: [
        Container(
          width: 46,
          height: 3,
          decoration: BoxDecoration(
            color: Colors.white24,
            borderRadius: BorderRadius.circular(10),
          ),
        ),
        const SizedBox(height: 12),
        Text(
          "Developed by Huraira Ejaz, Ali Raza, Syed Ali Wali Haider Naqvi",
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Colors.white.withOpacity(0.45),
            fontSize: 10,
            fontWeight: FontWeight.w600,
            letterSpacing: 1.1,
          ),
        ),
      ],
    );
  }
}


