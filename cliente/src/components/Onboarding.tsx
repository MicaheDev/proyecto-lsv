import { useState, useRef } from "react";
import { useNavigate } from "react-router";
const slides: any[] = [
  {
    id: "1",
    title: "¡Hola! Vamos a aprender señas juntos",
    imgSrc: "1.jpg",
  },

  {
    id: "2",
    title: "Mira el video y repite el movimiento",
    imgSrc: "2.gif",
  },

  {
    id: "3",
    title: "Usa tu cámara para que te ayudemos",
    imgSrc: "3.jpg",
  },
];
export default function Onboarding() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate()

  // Detectar en qué slide estamos al hacer scroll
  const handleScroll = () => {
    if (scrollRef.current) {
      const index = Math.round(
        scrollRef.current.scrollLeft / window.innerWidth,
      );
      setCurrentSlide(index);
    }
  };

  return (
    <div className="w-full h-svh flex flex-col overflow-hidden overflow-x-auto font-quicksand">
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="w-full h-full flex overflow-x-auto snap-x snap-mandatory scroll-smooth"
        style={{ scrollbarWidth: "none" }}
      >
        {slides.map((slide) => (
          <div
            className="w-screen snap-center gap-8 shrink-0 h-full flex flex-col justify-center items-center p-8"
            key={slide.id}
          >
            <h1 className="text-center text-4xl font-black">{slide.title}</h1>
            <img
              className="w-full h-60 object-cover rounded-4xl"
              src={slide.imgSrc}
            />
          </div>
        ))}
      </div>
      <div className="w-full flex flex-col gap-4 justify-center items-center p-8">
        <div className="flex gap-2">
          {slides.map((_, index) => (
            <div
              key={index}
              className={`h-2 rounded-full transition-all border duration-300 ${
                currentSlide === index ? "w-8 bg-amber-300" : "w-2 bg-gray-300"
              }`}
            />
          ))}
        </div>
        <button
          onClick={() => {
            if (currentSlide < slides.length - 1) {
              scrollRef.current?.scrollTo({
                left: window.innerWidth * (currentSlide + 1),
              });
            } else {
              console.log("Ir al Dashboard");
              navigate("/aprender")
            }
          }}
          className="w-full h-15 border font-black text-xl flex justify-center items-center bg-amber-300 rounded-2xl"
        >
          {currentSlide === slides.length - 1 ? "Empezar" : "Siguiente"}
        </button>
      </div>
    </div>
  );
}
