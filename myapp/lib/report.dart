import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Driving Report',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 255, 0, 0)),
        useMaterial3: true,
      ),
      home: const DriveReportPage(),
    );
  }
}

class DriveReportPage extends StatelessWidget {
  const DriveReportPage({super.key});

  @override
  Widget build(BuildContext context) {
    // Sample data for demonstration
    final String startLocation = "123 Start St, City A";
    final String endLocation = "456 End Ave, City B";
    final double distanceDriven = 15.3; // example distance in miles
    final double drivingScore = 92.5; // example score out of 100

    // Determine color based on driving score
    Color getScoreColor(double score) {
      if (score >= 85) {
        return Colors.green;
      } else if (score >= 60) {
        return Colors.yellow;
      } else {
        return Colors.red;
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('G.U.A.R.D. Drive Report'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 10,
                  offset: const Offset(0, 5),
                ),
              ],
              border: Border.all(color: const Color.fromARGB(255, 255, 0, 0), width: 2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  'Drive Summary',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                // Display start location
                Text(
                  'Start Location: $startLocation',
                  style: const TextStyle(fontSize: 18),
                ),
                const SizedBox(height: 10),
                // Display end location
                Text(
                  'End Location: $endLocation',
                  style: const TextStyle(fontSize: 18),
                ),
                const SizedBox(height: 10),
                // Display distance driven
                Text(
                  'Distance Driven: ${distanceDriven.toStringAsFixed(1)} miles',
                  style: const TextStyle(fontSize: 18),
                ),
                const SizedBox(height: 20),
                // Display driving score as a circular progress indicator
                Center(
                  child: Column(
                    children: [
                      SizedBox(
                        height: 150, // Increase the height of the circle
                        width: 150,  // Increase the width of the circle
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            CircularProgressIndicator(
                              value: drivingScore / 100, // percentage
                              strokeWidth: 12.0, // Thicker stroke for a larger dial
                              backgroundColor: Colors.grey[300],
                              valueColor: AlwaysStoppedAnimation<Color>(
                                  getScoreColor(drivingScore)),
                            ),
                            Text(
                              '${drivingScore.toStringAsFixed(1)}',
                              style: const TextStyle(
                                fontSize: 28, // Adjusted font size for clarity
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 10),
                      drivingScore >= 85
                          ? const Text(
                              'Great job! Your driving habits are safe and efficient.',
                              style: TextStyle(fontSize: 16, color: Colors.green),
                            )
                          : const Text(
                              'Consider keeping a safer distance and braking gradually.',
                              style: TextStyle(fontSize: 16, color: Colors.red),
                            ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
