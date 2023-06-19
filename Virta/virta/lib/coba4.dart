// import 'dart:convert';
// import 'dart:io';

// import 'package:flutter/material.dart';
// import 'package:image_picker/image_picker.dart';
// import 'package:http/http.dart' as http;
// import 'values.dart';


// class DashboardScreen extends StatefulWidget {
//   const DashboardScreen ({super.key});

//   @override
//   State<DashboardScreen> createState() => _DashboardScreenState();
// }

// class _DashboardScreenState extends State<DashboardScreen> {
//   bool isLoading = false;
//   late List<File> originalImage;
//   late List analyzedImage;

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text("Unggah gambar"),
//         actions: [
//           IconButton(
//             onPressed: () {
//               setState(() {
//                 originalImage = null;
//                 analyzedImage = null;
//               });
//             },
//             icon: const Icon(Icons.restart_alt_outlined),
//           ),
//         ],
//       ),
//       body: Center(
//         child: Column(
//           mainAxisSize: MainAxisSize.min,
//           children: [
//             const Text("Original Image"),
//             if (originalImage == null)
//               const Icon(Icons.image_outlined)
//             else
//               Row(
//                 children: [
//                   for (var image in originalImage) Image.file(image, height: 150),
//                 ],
//               ),
//             const SizedBox(height: 30),
//             const Text("Analyzed Image"),
//             if (isLoading) const CircularProgressIndicator(),
//             const SizedBox(height: 10),
//             if (analyzedImage == null)
//               const Icon(Icons.image_search_outlined)
//             else
//               Column(
//                 crossAxisAlignment: CrossAxisAlignment.start,
//                 children: [
//                   Text("BB Sistem : ${analyzedImage[0]} kg"),
//                   Text("Lingkar Kepala : ${analyzedImage[1]} cm"),
//                   Text("Tinggi : ${analyzedImage[2]} cm"),
//                 ],
//               ),
//           ],
//         ),
//       ),
//       floatingActionButton: FloatingActionButton(
//         child: const Icon(Icons.upload),
//         onPressed: () => analyzeImages(),
//       ),
//     );
//   }

//   Future<void> analyzeImages() async {
//     setState(() {
//       isLoading = true;
//     });
//     final files = await pickImages();
//     if (files != null) {
//       //store original image path
//       setState(() {
//         originalImage = files;
//       });
//       //start uploading
//       final result = await uploadImages(originalImage);
//       if (result != null) {
//         const snackBar = SnackBar(content: Text("Image uploaded"));
//         //check whether this screen is opened
//         if (mounted) ScaffoldMessenger.of(context).showSnackBar(snackBar);
//         setState(() {
//           analyzedImage = [result["BBSistem"], result["lingkarkepala"], result["tinggi"]];
//         });
//       } else {
//         const snackBar = SnackBar(content: Text("Image failed to be uploaded"));
//         if (mounted) ScaffoldMessenger.of(context).showSnackBar(snackBar);
//       }
//     }
//     setState(() {
//       isLoading = false;
//     });
//   }

//   Future<Map<String, dynamic>?> uploadImages(List<File> files) async {
//     final uri = Uri.parse("${Values.baseUrl}/test");

//     var request = http.MultipartRequest('POST', uri);
//     request.headers['ngrok-skip-browser-warning'] = 'true';

//     for (var file in files) {
//       request.files.add(await http.MultipartFile.fromPath(Values.field, file.path));
//     }

//     final response = await request.send();

//     final result = await http.Response.fromStream(response);

//     final jsonData = json.decode(result.body);

//     if (result.statusCode == 200) {
//       return jsonData;
//     } else {
//       return null;
//     }
//   }

//   Future<List<File>?> pickImages() async {
//     final ImagePicker picker = ImagePicker();
//     final images = await picker.pickMultiImage();
//     if (images.isNotEmpty) {
//       return images.map((image) => File(image.path)).toList();
//     } else {
//       return null;
//       }
//       }
// }