import 'package:flutter/material.dart';
import 'home.dart';
import 'report.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // Hides the debug banner
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MainPage(), // The entry page of your app
    );
  }
}

class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int index = 0;
  final screens = [
    HomePage(),
    DriveReportPage(),
  ];

  @override
  Widget build(BuildContext context) => Scaffold(
        body: screens[index],
        bottomNavigationBar: NavigationBarTheme(
          data: NavigationBarThemeData(
            indicatorColor: Colors.blue.shade300,
          ),
          child: NavigationBar(
            selectedIndex: index,
            onDestinationSelected: (index) => setState(() => this.index = index),
            destinations: const [
              NavigationDestination(
                icon: Icon(Icons.email_outlined),
                label: 'Mail',
              ),
              NavigationDestination(
                icon: Icon(Icons.chat_bubble_outline),
                label: 'Chat',
              ),
            ],
          ),
        ),
      );
}
