import 'dart:math';
import 'package:flutter/material.dart';
void main() {
  runApp(const RadarScreen());
}

class RadarScreen extends StatefulWidget {
  const RadarScreen({super.key});

  @override
  State<RadarScreen> createState() => _RadarScreenState();
}

class _RadarScreenState extends State<RadarScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final Random random = Random();
  final int numBlips = 10;
  final List<Offset> fixedBlips = [
    Offset(0.5 * cos(pi / 6), 0.5 * sin(pi / 6)), // 30°
    Offset(0.7 * cos(pi / 3), 0.7 * sin(pi / 3)), // 60°
    Offset(0.9 * cos(pi), 0.9 * sin(pi)),         // 180°
    Offset(0.4 * cos(5 * pi / 4), 0.4 * sin(5 * pi / 4)), // 225°
  ];
  // Blip positions
  late List<Offset> blips;

  @override
  void initState() {
    super.initState();

    // Random positions inside the radar circle
    blips = fixedBlips;

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 4),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width;
    double height = MediaQuery.of(context).size.height;
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: AnimatedBuilder(
            animation: _controller,
            builder: (_, __) {
              return CustomPaint(
                size:  Size(width*0.9, height*0.9),
                painter: RadarPainter(blips,angle: _controller.value * 2 * pi),
              );
            },
          ),
        ),
      ),
    );
  }
}

class RadarPainter extends CustomPainter {
  final double angle;
  final List<Offset> blips;


  RadarPainter(this.blips, {required this.angle});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    // Background
    final bgPaint = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius, bgPaint);

    // Grid circles
    final gridPaint = Paint()
      ..color = Colors.green.withOpacity(0.3)
      ..style = PaintingStyle.stroke;

    for (int i = 1; i <= 5; i++) {
      canvas.drawCircle(center, radius * i / 5, gridPaint);
    }

    // Cross lines
    canvas.drawLine(
      Offset(center.dx - radius, center.dy),
      Offset(center.dx + radius, center.dy),
      gridPaint,
    );
    canvas.drawLine(
      Offset(center.dx, center.dy - radius),
      Offset(center.dx, center.dy + radius),
      gridPaint,
    );

    // Radar sweep
    final sweepPaint = Paint()
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round
      ..shader = LinearGradient(
        begin: Alignment.center,
        end: Alignment(
          cos(angle + pi / 4),
          sin(angle + pi / 4),
        ),
        colors: [
          Colors.green.withOpacity(0.0),
          Colors.green.withOpacity(0.9),
          Colors.green,
        ],
      ).createShader(Rect.fromCircle(center: center, radius: radius));

// Draw a line from center to the tip of sweep
    canvas.drawLine(
      center,
      Offset(
        center.dx + radius * cos(angle),
        center.dy + radius * sin(angle),
      ),
      sweepPaint,
    );
    for (var blip in blips) {
      final blipPos = Offset(
        center.dx + blip.dx * radius,
        center.dy + blip.dy * radius,
      );

      double blipAngle = atan2(blip.dy, blip.dx);
      // If sweep is close to blip angle, show it
      double diff = (angle - blipAngle) % (2 * pi);
      if (diff < 0) diff += 2 * pi;

      if (diff < 0.2) {
        final paint = Paint()
          ..color = Colors.green
          ..style = PaintingStyle.fill;
        canvas.drawCircle(blipPos, 5, paint);
      }
    }


  }

  @override
  bool shouldRepaint(covariant RadarPainter oldDelegate) {
    return oldDelegate.angle != angle;
  }
}
