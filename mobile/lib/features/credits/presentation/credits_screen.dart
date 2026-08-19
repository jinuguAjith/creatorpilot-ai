import 'package:flutter/material.dart';

import '../../../core/theme/app_theme.dart';

class CreditsScreen extends StatelessWidget {
  const CreditsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Credits & Plan')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Free plan', style: TextStyle(fontWeight: FontWeight.w600)),
                    SizedBox(height: 4),
                    Text('12 credits remaining this month',
                        style: TextStyle(color: AppColors.textSecondary)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            // Phase 11: wire to in_app_purchase + backend purchase-token
            // verification. The client never grants entitlements itself.
            _PlanTile(name: 'Creator', price: '₹299/mo'),
            _PlanTile(name: 'Business', price: '₹999/mo'),
            _PlanTile(name: 'Pro', price: '₹2499/mo'),
          ],
        ),
      ),
    );
  }
}

class _PlanTile extends StatelessWidget {
  final String name;
  final String price;
  const _PlanTile({required this.name, required this.price});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text(price),
        trailing: OutlinedButton(onPressed: () {}, child: const Text('Upgrade')),
      ),
    );
  }
}
