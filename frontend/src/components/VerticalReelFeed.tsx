import React, { useRef, useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Volume2,
  VolumeX,
  Heart,
  MessageCircle,
  Send,
  MoreVertical,
} from "lucide-react";

import video1 from "../assets/videos/output_final.mp4"

type Reel = {
  id: number;
  user: string;
  description: string;
  music: string;
  likes: number;
  comments: number;
  shares: number;
  videoUrl: string;
  avatarUrl?: string;
};

const MOCK_REELS: Reel[] = [
  {
    id: 1,
    user: "louis.dev",
    description: "Test d’un vertical feed React 🎥",
    music: "Original sound - Louis",
    likes: 234,
    comments: 18,
    shares: 7,
    videoUrl: video1,
  },
  {
    id: 2,
    user: "react.ui",
    description: "Interface style TikTok avec Tailwind.",
    music: "Remix - UI",
    likes: 1042,
    comments: 99,
    shares: 31,
    videoUrl: video1,
  },
  {
    id: 3,
    user: "design.lab",
    description: "Animations Framer Motion ✨",
    music: "Chill beat",
    likes: 653,
    comments: 42,
    shares: 15,
    videoUrl: video1,
  },
];

const VerticalReelFeed: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [muted, setMuted] = useState<boolean>(true);
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRefs = useRef<HTMLVideoElement[]>([]);

  /* Active la vidéo visible */
  useEffect(() => {
    videoRefs.current.forEach((video, i) => {
      if (i === currentIndex) {
        video?.play().catch(() => {});
      } else {
        video?.pause();
        if (video) video.currentTime = 0;
      }
    });
  }, [currentIndex]);

  /* Détecte l’index en fonction du scroll */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const handleScroll = () => {
      const { scrollTop, clientHeight } = el;
      const index = Math.round(scrollTop / clientHeight);
      setCurrentIndex(Math.min(Math.max(index, 0), MOCK_REELS.length - 1));
    };

    el.addEventListener("scroll", handleScroll);
    return () => el.removeEventListener("scroll", handleScroll);
  }, []);

  const toggleMute = () => {
    setMuted(!muted);
    videoRefs.current.forEach((video) => (video.muted = !muted));
  };

  return (
    <div className="h-screen w-full bg-black flex items-center justify-center">
      <div
        ref={containerRef}
        className="relative h-screen w-full max-w-[480px] overflow-y-scroll snap-y snap-mandatory bg-black"
      >
        {MOCK_REELS.map((reel, index) => (
          <section
            key={reel.id}
            className="snap-start h-screen flex items-center justify-center relative"
          >
            {/* Vidéo */}
            <motion.video
              ref={(el) => {
                if (el) videoRefs.current[index] = el;
              }}
              src={reel.videoUrl}
              muted={muted}
              loop
              playsInline
              className="h-screen w-full object-contain object-top bg-black"
              initial={{ opacity: 0.6, scale: 1.02 }}
              animate={{
                opacity: index === currentIndex ? 1 : 0.8,
                scale: index === currentIndex ? 1 : 1.02,
              }}
              transition={{ duration: 0.3 }}
            />

            {/* Ombre bas */}
            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-56 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />

            {/* Infos vidéo */}
            <div className="absolute bottom-5 left-4 right-20 text-white space-y-2">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-white/20 flex items-center justify-center text-xs font-semibold">
                  {reel.user[0].toUpperCase()}
                </div>
                <span className="font-semibold text-sm">@{reel.user}</span>
                <button className="ml-2 px-3 py-1 rounded-full border border-white/40 text-xs font-semibold">
                  S’abonner
                </button>
              </div>

              <p className="text-sm leading-snug">{reel.description}</p>

              <div className="flex items-center gap-1 text-xs text-white/80">
                <span className="font-semibold">♫</span>
                <span className="truncate">{reel.music}</span>
              </div>
            </div>

            {/* Boutons droite */}
            <div className="absolute right-3 bottom-16 flex flex-col items-center gap-4 text-white">
              <button className="flex flex-col items-center gap-1">
                <div className="h-11 w-11 rounded-full bg-white/15 flex items-center justify-center">
                  <Heart className="h-5 w-5" />
                </div>
                <span className="text-xs">{reel.likes}</span>
              </button>

              <button className="flex flex-col items-center gap-1">
                <div className="h-11 w-11 rounded-full bg-white/15 flex items-center justify-center">
                  <MessageCircle className="h-5 w-5" />
                </div>
                <span className="text-xs">{reel.comments}</span>
              </button>

              <button className="flex flex-col items-center gap-1">
                <div className="h-11 w-11 rounded-full bg-white/15 flex items-center justify-center">
                  <Send className="h-5 w-5" />
                </div>
                <span className="text-xs">{reel.shares}</span>
              </button>

              <button className="flex flex-col items-center gap-1">
                <div className="h-9 w-9 rounded-full bg-white/15 flex items-center justify-center">
                  <MoreVertical className="h-4 w-4" />
                </div>
              </button>
            </div>

            {/* Mute bouton */}
            <button
              onClick={toggleMute}
              className="absolute right-4 top-5 h-9 w-9 rounded-full bg-black/50 flex items-center justify-center text-white"
            >
              {muted ? (
                <VolumeX className="h-5 w-5" />
              ) : (
                <Volume2 className="h-5 w-5" />
              )}
            </button>
          </section>
        ))}
      </div>
    </div>
  );
};

export default VerticalReelFeed;
