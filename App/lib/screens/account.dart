// import 'dart:io';
// import 'dart:convert'; // CHANGE: Added for JSON body
// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http; // CHANGE: Added for backend API call
// import 'package:shared_preferences/shared_preferences.dart'; // CHANGE: Added to update local saved user data
//
// import '../home_screen.dart' show kPrimaryColor, kAccentColor;
// import '../Account Screens/forgot_password_screen.dart' hide kPrimaryColor;
// import 'rating_screen.dart';
//
// // CHANGE: Import your API config file.
// // If your AppConfig file path is different, adjust this import.
// import '../config/app_config.dart';
//
// class AccountPage extends StatefulWidget {
//   final Future<Map<String, String>> Function() getUserInfo;
//   final String? profileImagePath;
//   final VoidCallback pickProfileImage;
//   final VoidCallback clearSession;
//   final VoidCallback deleteAccount;
//
//   const AccountPage({
//     super.key,
//     required this.getUserInfo,
//     required this.profileImagePath,
//     required this.pickProfileImage,
//     required this.clearSession,
//     required this.deleteAccount,
//   });
//
//   @override
//   State<AccountPage> createState() => _AccountPageState();
// }
//
// class _AccountPageState extends State<AccountPage> {
//   bool _passwordVisible = false;
//
//   // CHANGE: Controllers added for editable name and phone
//   final TextEditingController _nameController = TextEditingController();
//   final TextEditingController _phoneController = TextEditingController();
//
//   // CHANGE: State added for edit/save profile mode
//   bool _isEditingProfile = false;
//   bool _isSavingProfile = false;
//   bool _controllersFilled = false;
//
//   // CHANGE: Dispose controllers to avoid memory leak
//   @override
//   void dispose() {
//     _nameController.dispose();
//     _phoneController.dispose();
//     super.dispose();
//   }
//
//   // CHANGE: Save updated name and phone to backend database
//   Future<void> _saveProfileChanges() async {
//     final name = _nameController.text.trim();
//     final phone = _phoneController.text.trim();
//
//     if (name.isEmpty) {
//       _showMessage("Name cannot be empty");
//       return;
//     }
//
//     if (phone.isEmpty || !RegExp(r'^03\d{9}$').hasMatch(phone)) {
//       _showMessage("Enter valid phone number like 03123456789");
//       return;
//     }
//
//     setState(() {
//       _isSavingProfile = true;
//     });
//
//     try {
//       final prefs = await SharedPreferences.getInstance();
//       final token = prefs.getString("access_token");
//
//       final response = await http.patch(
//         Uri.parse("${AppConfig.baseUrl}/profile/update"),
//         headers: {
//           "Content-Type": "application/json",
//           if (token != null && token.isNotEmpty)
//             "Authorization": "Bearer $token",
//         },
//         body: jsonEncode({
//           "full_name": name,
//           "phone": phone,
//         }),
//       );
//
//       if (response.statusCode == 200) {
//         // CHANGE: Update local saved data also, otherwise old data may still show
//         await prefs.setString("name", name);
//         await prefs.setString("phone", phone);
//
//         setState(() {
//           _isEditingProfile = false;
//         });
//
//         _showMessage("Profile updated successfully");
//       } else {
//         final body = jsonDecode(response.body);
//         _showMessage(body["detail"]?.toString() ?? "Failed to update profile");
//       }
//     } catch (e) {
//       _showMessage("Error updating profile: $e");
//     } finally {
//       if (mounted) {
//         setState(() {
//           _isSavingProfile = false;
//         });
//       }
//     }
//   }
//
//   // CHANGE: Helper snackbar method
//   void _showMessage(String message) {
//     if (!mounted) return;
//     ScaffoldMessenger.of(context).showSnackBar(
//       SnackBar(content: Text(message)),
//     );
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return FutureBuilder<Map<String, String>>(
//       future: widget.getUserInfo(),
//       builder: (context, snapshot) {
//         if (!snapshot.hasData) {
//           return const Center(child: CircularProgressIndicator());
//         }
//
//         final data = snapshot.data!;
//         final name = data['name'] ?? 'User';
//         final email = data['email'] ?? 'N/A';
//         final password = data['password'] ?? '';
//         final phone = data['phone'] ?? 'N/A';
//
//         // CHANGE: Fill controllers only once, not on every rebuild
//         if (!_controllersFilled) {
//           _nameController.text = name;
//           _phoneController.text = phone == 'N/A' ? '' : phone;
//           _controllersFilled = true;
//         }
//
//         String? safeProfilePath =
//         (widget.profileImagePath == null ||
//             widget.profileImagePath!.isEmpty ||
//             widget.profileImagePath == "null")
//             ? null
//             : widget.profileImagePath;
//
//         return CustomScrollView(
//           slivers: [
//             SliverAppBar(
//               expandedHeight: 250.0,
//               pinned: true,
//               backgroundColor: kPrimaryColor,
//               automaticallyImplyLeading: false,
//               flexibleSpace: FlexibleSpaceBar(
//                 // CHANGE: App bar title now shows edited name live
//                 title: Text(
//                   _nameController.text.isNotEmpty
//                       ? _nameController.text
//                       : name,
//                   style: const TextStyle(
//                     color: Colors.white,
//                     fontWeight: FontWeight.bold,
//                   ),
//                 ),
//                 centerTitle: true,
//                 background: Padding(
//                   padding: const EdgeInsets.only(top: 20.0, bottom: 70.0),
//                   child: Center(
//                     child: Stack(
//                       children: [
//                         CircleAvatar(
//                           radius: 80,
//                           backgroundImage: safeProfilePath == null
//                               ? const AssetImage("assets/default_profile.png")
//                               : FileImage(File(safeProfilePath))
//                           as ImageProvider,
//                         ),
//                         Positioned(
//                           bottom: 0,
//                           right: 0,
//                           child: GestureDetector(
//                             onTap: widget.pickProfileImage,
//                             child: Container(
//                               padding: const EdgeInsets.all(4),
//                               decoration: BoxDecoration(
//                                 color: kPrimaryColor,
//                                 shape: BoxShape.circle,
//                                 border: Border.all(
//                                   color: Colors.white,
//                                   width: 2,
//                                 ),
//                               ),
//                               child: const Icon(
//                                 Icons.edit,
//                                 color: Colors.white,
//                                 size: 16,
//                               ),
//                             ),
//                           ),
//                         ),
//                       ],
//                     ),
//                   ),
//                 ),
//               ),
//             ),
//
//             SliverList(
//               delegate: SliverChildListDelegate([
//                 Padding(
//                   padding: const EdgeInsets.symmetric(horizontal: 20.0),
//                   child: Column(
//                     crossAxisAlignment: CrossAxisAlignment.stretch,
//                     children: [
//                       const SizedBox(height: 10),
//
//                       // CHANGE: Added editable profile card for name and phone
//                       Card(
//                         shape: RoundedRectangleBorder(
//                           borderRadius: BorderRadius.circular(15),
//                         ),
//                         elevation: 3,
//                         child: Padding(
//                           padding: const EdgeInsets.all(20),
//                           child: Column(
//                             crossAxisAlignment: CrossAxisAlignment.start,
//                             children: [
//                                Row(
//                                    children: [
//                                      Expanded(
//                                        child: Text(
//                                          "👤 Profile Information",
//                                          style: TextStyle(
//                                            fontWeight: FontWeight.bold,
//                                            fontSize: 18,
//                                          ),
//                                          overflow: TextOverflow.ellipsis,
//                                        ),
//                                      ),
//                                      TextButton.icon(
//                                        onPressed: _isSavingProfile ? null : () {
//                                          setState(() {
//                                            _isEditingProfile = !_isEditingProfile;
//
//                                            if (!_isEditingProfile) {
//                                               _nameController.text = name;
//                                               _phoneController.text = phone == 'N/A' ? '' : phone;
//                                            }
//                                          });
//                                        },
//                                        icon: Icon(
//                                          _isEditingProfile ? Icons.close : Icons.edit,
//                                          color: kPrimaryColor,
//                                        ),
//                                        label: Text(
//                                          _isEditingProfile ? "Cancel" : "Edit",
//                                          style: const TextStyle(
//                                            color: kPrimaryColor,
//                                            fontWeight: FontWeight.bold,
//                                          ),
//                                        ),
//                                      ),
//                                    ],
//                                  )
//
//                                   // CHANGE: Edit/Cancel button added
//                                   TextButton.icon(
//                                     onPressed: _isSavingProfile
//                                         ? null
//                                         : () {
//                                       setState(() {
//                                         _isEditingProfile =
//                                         !_isEditingProfile;
//
//                                         if (!_isEditingProfile) {
//                                           _nameController.text = name;
//                                           _phoneController.text =
//                                           phone == 'N/A' ? '' : phone;
//                                         }
//                                       });
//                                     },
//                                     icon: Icon(
//                                       _isEditingProfile
//                                           ? Icons.close
//                                           : Icons.edit,
//                                       color: kPrimaryColor,
//                                     ),
//                                     label: Text(
//                                       _isEditingProfile ? "Cancel" : "Edit",
//                                       style: const TextStyle(
//                                         color: kPrimaryColor,
//                                         fontWeight: FontWeight.bold,
//                                       ),
//                                     ),
//                                   ),
//                                 ],
//                               ),
//
//                               const SizedBox(height: 15),
//
//                               // CHANGE: Name is now editable
//                               TextField(
//                                 controller: _nameController,
//                                 enabled: _isEditingProfile,
//                                 decoration: InputDecoration(
//                                   focusedBorder: OutlineInputBorder(
//                                     borderRadius: BorderRadius.circular(12),
//                                     borderSide: const BorderSide(color: kPrimaryColor, width: 2),
//                                   ),
//                                   enabledBorder: OutlineInputBorder(
//                                     borderRadius: BorderRadius.circular(12),
//                                     borderSide: BorderSide(color: Colors.grey.shade300),
//                                   ),
//                                   labelText: "Full Name",
//                                   prefixIcon: const Icon(Icons.person),
//                                   border: OutlineInputBorder(
//                                     borderRadius: BorderRadius.circular(12),
//                                   ),
//                                 ),
//                                 onChanged: (_) {
//                                   setState(() {});
//                                 },
//                               ),
//
//                               const SizedBox(height: 15),
//
//                               // CHANGE: Phone is now editable
//                               TextField(
//                                 controller: _phoneController,
//                                 enabled: _isEditingProfile,
//                                 keyboardType: TextInputType.phone,
//                                 decoration: InputDecoration(
//                                   labelText: "Phone Number",
//                                   hintText: "03123456789",
//                                   prefixIcon: const Icon(Icons.phone),
//                                   border: OutlineInputBorder(
//                                     borderRadius: BorderRadius.circular(12),
//                                   ),
//                                 ),
//                               ),
//
//                               // CHANGE: Save button added
//                               if (_isEditingProfile) ...[
//                                 const SizedBox(height: 18),
//                                 SizedBox(
//                                   width: double.infinity,
//                                   child: ElevatedButton.icon(
//                                     onPressed: _isSavingProfile
//                                         ? null
//                                         : _saveProfileChanges,
//                                     icon: _isSavingProfile
//                                         ? const SizedBox(
//                                       width: 18,
//                                       height: 18,
//                                       child: CircularProgressIndicator(
//                                         strokeWidth: 2,
//                                         color: Colors.white,
//                                       ),
//                                     )
//                                         : const Icon(
//                                       Icons.save,
//                                       color: Colors.white,
//                                     ),
//                                     label: Text(
//                                       _isSavingProfile
//                                           ? "Saving..."
//                                           : "Save Changes",
//                                       style: const TextStyle(
//                                         fontSize: 16,
//                                         color: Colors.white,
//                                       ),
//                                     ),
//                                     style: ElevatedButton.styleFrom(
//                                       backgroundColor: kPrimaryColor,
//                                       padding: const EdgeInsets.symmetric(
//                                         vertical: 14,
//                                       ),
//                                       shape: RoundedRectangleBorder(
//                                         borderRadius: BorderRadius.circular(12),
//                                       ),
//                                     ),
//                                   ),
//                                 ),
//                               ],
//                             ],
//                           ),
//                         ),
//                       ),
//
//                       const SizedBox(height: 20),
//
//                       Card(
//                         shape: RoundedRectangleBorder(
//                           borderRadius: BorderRadius.circular(15),
//                         ),
//                         elevation: 3,
//                         child: Padding(
//                           padding: const EdgeInsets.all(20),
//                           child: Column(
//                             crossAxisAlignment: CrossAxisAlignment.start,
//                             children: [
//                               const Text(
//                                 "📧 Email",
//                                 style: TextStyle(
//                                   fontSize: 18,
//                                   fontWeight: FontWeight.bold,
//                                 ),
//                               ),
//                               const SizedBox(height: 8),
//                               Text(
//                                 email,
//                                 style: const TextStyle(fontSize: 16),
//                               ),
//                             ],
//                           ),
//                         ),
//                       ),
//
//                       const SizedBox(height: 20),
//
//                       // Card(
//                       //   shape: RoundedRectangleBorder(
//                       //     borderRadius: BorderRadius.circular(15),
//                       //   ),
//                       //   elevation: 3,
//                       //   child: Padding(
//                       //     padding: const EdgeInsets.all(20),
//                       //     child: Column(
//                       //       crossAxisAlignment: CrossAxisAlignment.start,
//                       //       children: [
//                       //         const Text(
//                       //           "🔐 Password",
//                       //           style: TextStyle(
//                       //             fontWeight: FontWeight.bold,
//                       //             fontSize: 18,
//                       //           ),
//                       //         ),
//                       //         const SizedBox(height: 8),
//                       //
//                       //         // CHANGE: Password is not directly editable here.
//                       //         // Use Reset Password because backend must hash password securely.
//                       //         Row(
//                       //           mainAxisAlignment:
//                       //           MainAxisAlignment.spaceBetween,
//                       //           children: [
//                       //             Expanded(
//                       //               child: Text(
//                       //                 password.isNotEmpty
//                       //                     ? (_passwordVisible
//                       //                     ? password
//                       //                     : "*" * password.length)
//                       //                     : "Use reset password to change it",
//                       //                 style: const TextStyle(fontSize: 16),
//                       //                 overflow: TextOverflow.ellipsis,
//                       //               ),
//                       //             ),
//                       //             IconButton(
//                       //               icon: Icon(
//                       //                 _passwordVisible
//                       //                     ? Icons.visibility_off
//                       //                     : Icons.visibility,
//                       //                 color: Colors.grey,
//                       //               ),
//                       //               onPressed: () {
//                       //                 setState(() {
//                       //                   _passwordVisible = !_passwordVisible;
//                       //                 });
//                       //               },
//                       //             ),
//                       //           ],
//                       //         ),
//                       //       ],
//                       //     ),
//                       //   ),
//                       // ),
//
//                       // CHANGE: Added Rate QueryMate option
//                       const SizedBox(height: 20),
//
//                       Card(
//                         shape: RoundedRectangleBorder(
//                           borderRadius: BorderRadius.circular(15),
//                         ),
//                         elevation: 3,
//                         child: ListTile(
//                           leading: const Icon(
//                             Icons.star_rate,
//                             color: kPrimaryColor,
//                           ),
//                           title: const Text(
//                             "Rate QueryMate",
//                             style: TextStyle(fontWeight: FontWeight.bold),
//                           ),
//                           trailing:
//                           const Icon(Icons.arrow_forward_ios, size: 16),
//                           onTap: () {
//                             Navigator.push(
//                               context,
//                               MaterialPageRoute(
//                                 builder: (_) => const RatingScreen(),
//                               ),
//                             );
//                           },
//                         ),
//                       ),
//
//                       const SizedBox(height: 20),
//
//                       SizedBox(
//                         width: double.infinity,
//                         child: ElevatedButton.icon(
//                           onPressed: () {
//                             Navigator.push(
//                               context,
//                               MaterialPageRoute(
//                                 builder: (context) =>
//                                 const ForgotPasswordScreen(),
//                               ),
//                             );
//                           },
//                           icon: const Icon(
//                             Icons.lock_reset,
//                             color: Colors.white,
//                           ),
//                           label: const Text(
//                             "Reset Password",
//                             style: TextStyle(
//                               fontSize: 18,
//                               color: Colors.white,
//                             ),
//                           ),
//                           style: ElevatedButton.styleFrom(
//                             backgroundColor: kPrimaryColor,
//                             padding: const EdgeInsets.symmetric(vertical: 14),
//                             shape: RoundedRectangleBorder(
//                               borderRadius: BorderRadius.circular(12),
//                             ),
//                           ),
//                         ),
//                       ),
//
//                       const SizedBox(height: 40),
//
//                       Row(
//                         children: [
//                           Expanded(
//                             child: ElevatedButton.icon(
//                               onPressed: () {
//                                 widget.clearSession();
//                                 if (context.mounted) {
//                                   Navigator.pushReplacementNamed(context, '/launch');
//                                 }
//                               },
//                               icon: const Icon(
//                                 Icons.logout,
//                                 color: Colors.white,
//                               ),
//                               label: const Text(
//                                 "Logout",
//                                 style: TextStyle(
//                                   fontSize: 16,
//                                   color: Colors.white,
//                                 ),
//                               ),
//                               style: ElevatedButton.styleFrom(
//                                 backgroundColor: kPrimaryColor,
//                                 padding: const EdgeInsets.symmetric(
//                                   vertical: 14,
//                                 ),
//                                 shape: RoundedRectangleBorder(
//                                   borderRadius: BorderRadius.circular(12),
//                                 ),
//                               ),
//                             ),
//                           ),
//                           const SizedBox(width: 12),
//                           Expanded(
//                             child: ElevatedButton.icon(
//                               onPressed: widget.deleteAccount,
//                               icon: const Icon(
//                                 Icons.delete_forever,
//                                 color: Colors.white,
//                               ),
//                               label: const Text(
//                                 "Delete Account",
//                                 style: TextStyle(
//                                   fontSize: 16,
//                                   color: Colors.white,
//                                 ),
//                               ),
//                               style: ElevatedButton.styleFrom(
//                                 backgroundColor: kAccentColor,
//                                 padding: const EdgeInsets.symmetric(
//                                   vertical: 14,
//                                 ),
//                                 shape: RoundedRectangleBorder(
//                                   borderRadius: BorderRadius.circular(12),
//                                 ),
//                               ),
//                             ),
//                           ),
//                         ],
//                       ),
//
//                       const SizedBox(height: 150),
//                     ],
//                   ),
//                 ),
//               ]),
//             ),
//           ],
//         );
//       },
//     );
//   }
// }


import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../home_screen.dart' show kPrimaryColor, kAccentColor;
import '../Account Screens/forgot_password_screen.dart' hide kPrimaryColor;
import 'rating_screen.dart';
import '../config/app_config.dart';

class AccountPage extends StatefulWidget {
  final Future<Map<String, String>> Function() getUserInfo;
  final String? profileImagePath;
  final VoidCallback pickProfileImage;
  final VoidCallback clearSession;
  final VoidCallback deleteAccount;

  const AccountPage({
    super.key,
    required this.getUserInfo,
    required this.profileImagePath,
    required this.pickProfileImage,
    required this.clearSession,
    required this.deleteAccount,
  });

  @override
  State<AccountPage> createState() => _AccountPageState();
}

class _AccountPageState extends State<AccountPage> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();

  bool _isEditingProfile = false;
  bool _isSavingProfile = false;
  bool _controllersFilled = false;

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  Future<void> _saveProfileChanges() async {
    final name = _nameController.text.trim();
    final phone = _phoneController.text.trim();

    if (name.isEmpty) {
      _showMessage("Name cannot be empty");
      return;
    }

    if (!RegExp(r'^03\d{9}$').hasMatch(phone)) {
      _showMessage("Enter valid phone number like 03123456789");
      return;
    }

    setState(() => _isSavingProfile = true);

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString("access_token");

      final response = await http.patch(
        Uri.parse("${AppConfig.baseUrl}/profile/update"),
        headers: {
          "Content-Type": "application/json",
          if (token != null) "Authorization": "Bearer $token",
        },
        body: jsonEncode({
          "full_name": name,
          "phone": phone,
        }),
      );

      if (response.statusCode == 200) {
        await prefs.setString("name", name);
        await prefs.setString("phone", phone);

        setState(() => _isEditingProfile = false);
        _showMessage("Profile updated successfully");
      } else {
        final body = jsonDecode(response.body);
        _showMessage(body["detail"] ?? "Update failed");
      }
    } catch (e) {
      _showMessage("Error: $e");
    } finally {
      if (mounted) {
        setState(() => _isSavingProfile = false);
      }
    }
  }

  void _showMessage(String msg) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(msg)));
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, String>>(
      future: widget.getUserInfo(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Center(child: CircularProgressIndicator());
        }

        final data = snapshot.data!;
        final name = data['name'] ?? 'User';
        final email = data['email'] ?? 'N/A';
        final phone = data['phone'] ?? 'N/A';

        if (!_controllersFilled) {
          _nameController.text = name;
          _phoneController.text = phone == 'N/A' ? '' : phone;
          _controllersFilled = true;
        }

        final safeProfilePath =
        (widget.profileImagePath == null ||
            widget.profileImagePath!.isEmpty ||
            widget.profileImagePath == "null")
            ? null
            : widget.profileImagePath;

        return CustomScrollView(
          slivers: [
            SliverAppBar(
              expandedHeight: 250,
              pinned: true,
              backgroundColor: kPrimaryColor,
              automaticallyImplyLeading: false,
              flexibleSpace: FlexibleSpaceBar(
                title: Text(
                  _nameController.text,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                ),
                centerTitle: true,
                background: Center(
                  child: Stack(
                    children: [
                      CircleAvatar(
                        radius: 70,
                        backgroundImage: safeProfilePath == null
                            ? const AssetImage("assets/default_profile.png")
                            : FileImage(File(safeProfilePath))
                        as ImageProvider,
                      ),
                      Positioned(
                        bottom: 0,
                        right: 0,
                        child: GestureDetector(
                          onTap: widget.pickProfileImage,
                          child: Container(
                            padding: const EdgeInsets.all(6),
                            decoration: BoxDecoration(
                              color: kPrimaryColor,
                              shape: BoxShape.circle,
                              border:
                              Border.all(color: Colors.white, width: 2),
                            ),
                            child: const Icon(Icons.edit,
                                size: 16, color: Colors.white),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // BODY
            SliverList(
              delegate: SliverChildListDelegate([
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      // PROFILE CARD
                      Card(
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15)),
                        elevation: 3,
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            children: [
                              Row(
                                children: [
                                  const Expanded(
                                    child: Text(
                                      "👤 Profile Information",
                                      style: TextStyle(
                                          fontSize: 18,
                                          fontWeight: FontWeight.bold),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                  TextButton.icon(
                                    onPressed: _isSavingProfile
                                        ? null
                                        : () {
                                      setState(() {
                                        _isEditingProfile =
                                        !_isEditingProfile;
                                      });
                                    },
                                    icon: Icon(
                                      _isEditingProfile
                                          ? Icons.close
                                          : Icons.edit,
                                      color: kPrimaryColor,
                                    ),
                                    label: Text(
                                      _isEditingProfile
                                          ? "Cancel"
                                          : "Edit",
                                      style: const TextStyle(
                                          color: kPrimaryColor),
                                    ),
                                  ),
                                ],
                              ),

                              const SizedBox(height: 15),

                              TextField(
                                controller: _nameController,
                                enabled: _isEditingProfile,
                                decoration: const InputDecoration(
                                  labelText: "Full Name",
                                  prefixIcon: Icon(Icons.person),
                                ),
                              ),

                              const SizedBox(height: 15),

                              TextField(
                                controller: _phoneController,
                                enabled: _isEditingProfile,
                                keyboardType: TextInputType.phone,
                                decoration: const InputDecoration(
                                  labelText: "Phone",
                                  prefixIcon: Icon(Icons.phone),
                                ),
                              ),

                              if (_isEditingProfile) ...[
                                const SizedBox(height: 15),
                                ElevatedButton(
                                  onPressed: _isSavingProfile
                                      ? null
                                      : _saveProfileChanges,
                                  child: _isSavingProfile
                                      ? const CircularProgressIndicator()
                                      : const Text("Save Changes"),
                                )
                              ]
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      // EMAIL CARD
                      Card(
                        child: ListTile(
                          leading: const Icon(Icons.email),
                          title: const Text("Email"),
                          subtitle: Text(email),
                        ),
                      ),

                      const SizedBox(height: 20),

                      // RESET PASSWORD
                      ElevatedButton.icon(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (_) =>
                                const ForgotPasswordScreen()),
                          );
                        },
                        icon: const Icon(Icons.lock_reset),
                        label: const Text("Reset Password"),
                      ),

                      const SizedBox(height: 20),

                      // ACTIONS
                      Row(
                        children: [
                          Expanded(
                            child: ElevatedButton(
                              onPressed: () {
                                widget.clearSession();
                                Navigator.pushReplacementNamed(
                                    context, '/launch');
                              },
                              child: const Text("Logout"),
                            ),
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  backgroundColor: kAccentColor),
                              onPressed: widget.deleteAccount,
                              child: const Text("Delete"),
                            ),
                          ),
                        ],
                      )
                    ],
                  ),
                )
              ]),
            )
          ],
        );
      },
    );
  }
}