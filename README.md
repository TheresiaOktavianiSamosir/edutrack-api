# EduTrack API

Backend REST API untuk EduTrack, sebuah platform LMS (Learning Management System) sederhana yang membantu mahasiswa memulai dan tetap konsisten belajar secara mandiri, khususnya di masa libur, dengan menyediakan kursus dan materi belajar yang tersusun bertahap serta pelacak progres.

## Status
🚧 Dalam pengembangan aktif. Tahap saat ini: perencanaan produk selesai, implementasi REST API sedang berjalan.

## Latar Belakang
Banyak mahasiswa merasa memiliki banyak waktu luang saat libur, tapi justru sulit memulai belajar hal baru karena tidak adanya struktur atau target yang jelas. EduTrack dirancang untuk menjawab masalah ini dengan menyediakan kursus dan materi terstruktur, lengkap dengan pelacak progres.

## Fitur (Scope)
- Autentikasi pengguna (register/login) dengan role admin dan student
- CRUD Course (kursus dan info lomba)
- CRUD Materi per kursus
- Enrollment kursus oleh student
- Penandaan materi selesai
- Dashboard progres belajar

## Tech Stack (Rencana)
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Autentikasi:** JWT
- **Version Control:** Git & GitHub

## Proses Pengembangan
Project ini dikembangkan dengan alur kerja product/project management sederhana:
1. Product Requirement Document (PRD)
2. User Story & Acceptance Criteria per fitur
3. Backlog dibagi ke Sprint 1 dan Sprint 2
4. Implementasi bertahap sesuai sprint

## Project Terkait
- `edutrack-web` — Web admin (Next.js) — akan datang
- `edutrack-mobile` — Mobile app student (Flutter) — akan datang

## Author
Theresia Oktaviani Samosir
