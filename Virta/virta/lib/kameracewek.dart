import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:virta/values.dart';
import 'package:http/http.dart' as http;

class Camera extends StatefulWidget {
  const Camera({super.key});

  @override
  State<Camera> createState() => _CameraState();
}

class _CameraState extends State<Camera> {
  File? imageFile;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.orange,
        title: const Text('Capturing Image'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            if (imageFile != null)
              Container(
                width: 300,
                height: 400,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: Colors.grey,
                  image: DecorationImage(
                      image: FileImage(imageFile!), fit: BoxFit.cover),
                  border: Border.all(width: 8, color: Colors.black12),
                  borderRadius: BorderRadius.circular(12.0),
                ),
              ),
            const SizedBox(
              height: 20,
            ),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () => getImage(source: ImageSource.camera),
                    child: const Text(
                      'Capture Image',
                      style: TextStyle(fontSize: 18),
                    ),
                  ),
                ),
                const SizedBox(
                  width: 20,
                ),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () => getImage(source: ImageSource.gallery),
                    child: const Text(
                      'Selected Image',
                      style: TextStyle(fontSize: 18),
                    ),
                  ),
                )
              ],
            )
          ],
        ),
      ),
    );
  }

  void getImage({required ImageSource source}) async {
    final file = await ImagePicker().pickImage(
      source: source,
      maxWidth: 640,
      maxHeight: 480,
    );

    if (file?.path != null) {
      setState(() {
        imageFile = File(file!.path);
      });
    }
  }
}

Future<Map<String, dynamic>?> uploadImages(List<File> files) async {
  final uri = Uri.parse("${Values.baseUrl}/test");

  var request = http.MultipartRequest('POST', uri);

  for (var file in files) {
    request.files
        .add(await http.MultipartFile.fromPath(Values.field, file.path));
  }

  final response = await request.send();

  final result = await http.Response.fromStream(response);

  final jsonData = json.decode(result.body);

  if (result.statusCode == 200) {
    return jsonData;
  } else {
    return null;
  }
}
