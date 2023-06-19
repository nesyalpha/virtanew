// import 'dart:convert';

// import 'dart:io';
// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import 'package:image_picker/image_picker.dart';
// import 'package:virta/kameracewek.dart';
// import 'package:virta/values.dart';

// class Camera extends StatefulWidget {
//   const Camera({super.key});

//   @override
//   State<Camera> createState() => _CameraState();
// }

// class _CameraState extends State<Camera> {
//   List<File>? originalImage;
//   bool isLoading = false;
//   List? analyzedImage;

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text("Ambil Gambar"),
//         actions: [
//           IconButton(
//             onPressed: () {
//               setState(() {
//                 originalImage = null;
//                 analyzedImage = null;
//               });
//             },
//             icon: const Icon(Icons.restart_alt_outlined),
//           )
//         ],
//       ),
//       body: Center(
//         child: Column(
//           children: [
//             const Text("Original Image"),
//             if (originalImage == null)
//               const Icon(Icons.image_outlined)
//             else
//               Row(
//                 children: [
//                   for (var image in originalImage!)
//                     Image.file(
//                       image,
//                       height: 150,
//                     ),
//                 ],
//               ),
//             const SizedBox(
//               height: 30,
//             ),
//             const Text("Analyzed Image"),
//             if (isLoading) const CircularProgressIndicator(),
//             const SizedBox(
//               height: 10,
//             ),
//             if (analyzedImage == null)
//               const Icon(Icons.image_search_outlined)
//             else
//               Column(
//                 crossAxisAlignment: CrossAxisAlignment.start,
//                 children: [
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                   Text(""),
//                 ],
//               )
//           ],
//         ),
//       ),
//       floatingActionButton: FloatingActionButton(
//         child: const Icon(Icons.upload),
//         onPressed: () => analyzedImage,
//       ),
//     );
//   }

//   Future<void> analyzedImages() async {
//     setState(() {
//       isLoading = true;
//     });
//     final file = await pickImage();
//     if (file != null) {
//       setState(() {
//         originalImage = file;
//       });

//       final result = await uploadImages(originalImage!);
//       if (result ! = null){
//         const SnackBar(content: Text("Image Uploaded"));
//         if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(snackBar);
//         setState(() {
//           analyzedImage = [result[""], result[""],result[""], result[""],result[""], result[""],result[""], result[""],result[""], result[""],];
//         });
//       } else{
//         const SnackBar(content: Text("Image Failed to be Uploaded"));
//         if(context.mounted) ScaffoldMessenger.of(context).showSnackBar(snackBar);
//       }
//     }
//     setState(() {
//       isLoading = false;
//     });
//   }

//   Future<Map<String,dynamic>?> uploadImage(List<File> files) async {
//     final uri = Uri.parse("${Values.baseUrl}/test");
//     var request = http.MultipartRequest('POST', uri);
//     for(var file in files){
//       request.files.add(await http.MultipartFile.fromPath(Values.field, file.path));
//     }
//     final response = await request.send();
//     final result = await http.Response.fromStream(response);
//     final jsonData = json.decode(result.body);
//     if(result.statusCode == 200){
//       return jsonData;
//     }else{
//       return null;
//     }
//   }

//   Future <File?> pickImage() async {
//     final ImagePicker picker = ImagePicker();
//     final images = await picker.pickImage();
//     if(images.isNotEmpty){
//       return images.map((image)=>File(image.path)).toList();
//     }else{
//       return null;
//     }
//   }


// }
