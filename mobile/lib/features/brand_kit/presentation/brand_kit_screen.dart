import 'package:flutter/material.dart';

class BrandKitScreen extends StatelessWidget {
  const BrandKitScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Phase 9: persist to Firestore `brand_kits/{userId}` and auto-attach
    // to every CampaignRequest sent from create_campaign_screen.
    return Scaffold(
      appBar: AppBar(title: const Text('Brand Kit')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: const [
            _Field(label: 'Business name'),
            _Field(label: 'Website'),
            _Field(label: 'Phone'),
            _Field(label: 'Address'),
            _Field(label: 'Brand description', maxLines: 3),
          ],
        ),
      ),
    );
  }
}

class _Field extends StatelessWidget {
  final String label;
  final int maxLines;
  const _Field({required this.label, this.maxLines = 1});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextField(
        maxLines: maxLines,
        decoration: InputDecoration(labelText: label),
      ),
    );
  }
}
