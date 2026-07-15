"use client";

import { motion } from "framer-motion";
import { MessageCircle, Smartphone, Brain } from "lucide-react";
import Link from "next/link";
import Image from "next/image";

// --- PROFESSIONAL COLOR PALETTE ---
const Colors = {
  Primary: "#0C164D", // Deep Indigo/Navy
  Secondary: "#0D9488", // Deep Teal/Cyan
  Accent: "#34D399", // Bright Mint/Emerald
  Background: "#F4F9FF", // Very Light Blue/Off-White
  TextDark: "#1F2937", // Dark Gray Text
  TextLight: "#E5E7EB", // Light Gray Text
};

export default function Home() {
  return (
    <main className={`min-h-screen text-[${Colors.TextDark}] scroll-smooth bg-[#0C164D]`}>
      {/* ✅ Navbar */}
      <header className={`fixed top-0 left-0 w-full bg-linear-to-br from-[${Colors.Primary}] to-[#1A3172] text-[${Colors.TextLight}] px-4 shadow-xl z-50 backdrop-blur-md`}>
        <nav className="flex items-center justify-between max-w-7xl mx-auto px-4 md:px-6 py-4">
          <div className="flex items-center">
            <Image 
              src="/mainlogo.svg" 
              alt="QueryMate Logo" 
              width={35} 
              height={35} 
              priority 
              className="mr-3" 
            />
            <h1 className={`text-xl md:text-2xl font-black tracking-tighter text-[${Colors.Accent}]`}>
              QueryMate
            </h1>
          </div>
          
          <div className="hidden lg:flex space-x-10 text-sm font-bold uppercase tracking-widest">
            <a href="#home" className={`hover:text-[${Colors.Accent}] transition duration-300`}>Home</a>
            <a href="#features" className={`hover:text-[${Colors.Accent}] transition duration-300`}>Features</a>
            <a href="#how" className={`hover:text-[${Colors.Accent}] transition duration-300`}>How It Works</a>
            <a href="#contact" className={`hover:text-[${Colors.Accent}] transition duration-300`}>Contact</a>
          </div>

          <Link
            href="/login"
            className={`bg-[${Colors.Secondary}] text-white px-6 py-2.5 rounded-full text-sm font-bold shadow-lg hover:scale-105 active:scale-95 transition-all duration-300`}
          >
            Login
          </Link>
        </nav>
      </header>

      {/* ✅ Hero Section */}
      <section
        id="home"
        className={`flex flex-col items-center justify-center text-center min-h-screen pt-32 pb-20 px-6 bg-linear-to-br from-[${Colors.Primary}] to-[#1A3172] text-[${Colors.TextLight}]`}
      >
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-4xl md:text-7xl lg:text-8xl font-black mb-8 leading-[1.2] md:leading-[1.1] tracking-tight max-w-5xl w-full wrap-break-word"
        >
          Instant Answers for <span className={`text-[${Colors.Accent}] block md:inline`}>Academic Success.</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className={`max-w-2xl text-base md:text-xl text-[${Colors.TextLight}]/80 mb-12 leading-relaxed font-medium px-2`}
        >
          QueryMate provides AI-powered, context-aware responses to all academic and administrative questions via Mobile or WhatsApp.
        </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          > Web Portal is only For Admin to handle the System</motion.div>
        {/* <div className="flex flex-col sm:flex-row gap-5 w-full sm:w-auto">
          <button className={`w-full sm:w-auto border-2 border-[${Colors.Accent}] text-[${Colors.Accent}] font-bold px-10 py-4 rounded-full text-lg shadow-2xl hover:bg-[${Colors.Accent}] hover:text-[${Colors.Primary}] transition-all duration-300 transform hover:-translate-y-1`}>
            Start Querying Now
          </button>
          <button className={`w-full sm:w-auto border-2 border-white text-white font-bold px-10 py-4 rounded-full text-lg shadow-2xl hover:bg-white hover:text-[${Colors.Primary}] transition-all duration-300 transform hover:-translate-y-1`}>
            Try on WhatsApp
          </button>
        </div> */}
      </section>

      {/* ✅ Features */}
      <section id="features" className="py-32 px-6 bg-[#02123b]">
        <div className="max-w-7xl mx-auto">
          <h2 className={`text-4xl md:text-5xl font-black text-center mb-20 text-white tracking-tight`}>
            The Edge of <span className={`text-[${Colors.Accent}]`}>QueryMate</span>
          </h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<MessageCircle className={`w-10 h-10 text-[${Colors.Accent}]`} />}
              title="Instant Accuracy"
              text="Get AI-generated responses to academic and administrative questions in seconds, sourced from official documents."
            />
            <FeatureCard
              icon={<Smartphone className={`w-10 h-10 text-[${Colors.Accent}]`} />}
              title="Multi-Platform"
              text="Available via Dedicated Mobile App and direct WhatsApp integration for maximum student convenience."
            />
            <FeatureCard
              icon={<Brain className={`w-10 h-10 text-[${Colors.Accent}]`} />}
              title="Intelligence"
              text="Understands course details and department policies for highly personalized and accurate replies."
            />
          </div>
        </div>
      </section>

      {/* ✅ How It Works */}
      <section id="how" className="py-32 px-6 bg-[#06194d] text-center">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-black mb-20 text-white tracking-tight">
            How The <span className={`text-[${Colors.Accent}]`}>Process Works</span>
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <StepCard
              number="01"
              title="Submit Your Query"
              text="Students or guests send their question via the app or WhatsApp. No complex menus required."
            />
            <StepCard
              number="02"
              title="AI Contextualizes"
              text="Our engine analyzes the query and cross-references internal databases for the most relevant info."
            />
            <StepCard
              number="03"
              title="Receive Precise Answer"
              text="Users get a quick response with direct links to official policies or supporting documents."
            />
          </div>
        </div>
      </section>

      {/* ✅ Footer */}
      <footer id="contact" className={`bg-[#031c5d] text-white text-center py-16 border-t border-white/10`}>
        <div className="max-w-7xl mx-auto px-6">
          <h3 className="font-black text-2xl mb-4 tracking-tight">QueryMate © 2025</h3>
          <p className={`text-[${Colors.TextLight}]/60 text-base font-medium max-w-md mx-auto`}>
            Developed by Huraira Ejaz & Team | University of Gujrat
          </p>
          <div className={`inline-block mt-8 px-6 py-2 rounded-full border border-[${Colors.Accent}]/30`}>
             <p className={`text-[${Colors.Accent}] text-sm font-bold`}>
               Contact: hurairaejaz62@gmail.com
             </p>
          </div>
        </div>
      </footer>
    </main>
  );
}

function FeatureCard({ icon, title, text }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className={`p-10 bg-[#0C164D] rounded-3xl border border-white/5 shadow-2xl hover:border-[${Colors.Accent}]/50 transition-all duration-500 group`}
    >
      <div className="mb-6 transform group-hover:scale-110 transition-transform duration-300">{icon}</div>
      <h3 className={`text-2xl font-bold mb-4 text-white`}>{title}</h3>
      <p className={`text-[${Colors.TextLight}]/70 leading-relaxed font-medium`}>{text}</p>
    </motion.div>
  );
}

function StepCard({ number, title, text }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      className={`bg-[#02123b] p-10 rounded-3xl shadow-2xl border-b-4 border-[${Colors.Secondary}] text-left h-full transition-transform hover:-translate-y-2`}
    >
      <div className={`text-[${Colors.Accent}] text-5xl font-black mb-6 opacity-40`}>{number}</div>
      <h3 className={`text-2xl font-bold mb-4 text-white`}>{title}</h3>
      <p className={`text-[${Colors.TextLight}]/70 leading-relaxed font-medium`}>{text}</p>
    </motion.div>
  );
}