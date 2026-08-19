import 'package:flutter/material.dart';

import '../../../core/theme/app_theme.dart';

class ProjectHistoryScreen extends StatelessWidget {
  const ProjectHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Phase 8: replace with StreamBuilder over
    // ProjectsRepository.watchProjects(userId) backed by Firestore
    // `projects` collection, ordered by creation date.
    return Scaffold(
      appBar: AppBar(title: const Text('Projects')),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(32),
          child: Text(
            'No campaigns yet. Once you generate content it will appear '
            'here with options to preview, download, share, regenerate or delete.',
            textAlign: TextAlign.center,
            style: TextStyle(color: AppColors.textSecondary),
          ),
        ),
      ),
    );
  }
}
