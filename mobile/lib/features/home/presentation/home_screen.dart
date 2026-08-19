import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_theme.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CreatorPilot AI'),
        actions: [
          IconButton(
            icon: const Icon(Icons.bolt_outlined),
            tooltip: 'Credits',
            onPressed: () => context.push('/credits'),
          ),
        ],
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            _CreateCampaignCard(onTap: () => context.push('/campaign/new')),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Recent Projects', style: Theme.of(context).textTheme.titleMedium),
                TextButton(
                  onPressed: () => context.push('/projects'),
                  child: const Text('View all'),
                ),
              ],
            ),
            const SizedBox(height: 12),
            // Phase 8 replaces this with a live Firestore-backed list.
            const _EmptyProjectsPlaceholder(),
            const SizedBox(height: 24),
            _QuickLinkTile(
              icon: Icons.palette_outlined,
              title: 'Brand Kit',
              subtitle: 'Save your logo, colours and details once',
              onTap: () => context.push('/brand-kit'),
            ),
          ],
        ),
      ),
    );
  }
}

class _CreateCampaignCard extends StatelessWidget {
  final VoidCallback onTap;
  const _CreateCampaignCard({required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(24),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [AppColors.primary, AppColors.primaryDark],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(24),
        ),
        child: Row(
          children: [
            const Icon(Icons.auto_awesome, color: Colors.white, size: 32),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('Create New Campaign',
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.w700, fontSize: 18)),
                  SizedBox(height: 4),
                  Text('Describe your idea. We handle the rest.',
                      style: TextStyle(color: Colors.white70)),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios, color: Colors.white, size: 16),
          ],
        ),
      ),
    );
  }
}

class _EmptyProjectsPlaceholder extends StatelessWidget {
  const _EmptyProjectsPlaceholder();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceCard,
        borderRadius: BorderRadius.circular(16),
      ),
      child: const Text(
        'No campaigns yet. Your first generated poster or video will show up here.',
        style: TextStyle(color: AppColors.textSecondary),
      ),
    );
  }
}

class _QuickLinkTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _QuickLinkTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: AppColors.accent),
        title: Text(title),
        subtitle: Text(subtitle, style: const TextStyle(color: AppColors.textSecondary)),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
