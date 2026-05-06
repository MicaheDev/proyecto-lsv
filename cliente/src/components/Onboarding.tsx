import {useState, useRef} from "react"
const slides: any[] = [
  {
    id: "1",
    title: "Bienvenido a LingoHands",
  imgSrc: "1.png"
    
  },
  
    {
    id: "2",
    title: "Aprende lengua de señas venezolana",
  imgSrc: "2.png"
    
  },
  
      {
    id: "3",
    title: "Unete ya a nosotros",
  imgSrc: "3.png"
    
  }
  ]
export default function Onboarding(){
const [currentSlide, setCurrentSlide] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Detectar en qué slide estamos al hacer scroll
  const handleScroll = () => {
    if (scrollRef.current) {
      const index = Math.round(scrollRef.current.scrollLeft / window.innerWidth);
      setCurrentSlide(index);
    }
  };
  
  return <div className="w-full h-svh flex flex-col overflow-hidden overflow-x-auto font-quicksand">
    
    <div 
    ref={scrollRef}
    onScroll={handleScroll}
    className="w-full h-full flex overflow-x-auto snap-x snap-mandatory scroll-smooth"
style={{ scrollbarWidth: 'none' }} 
    >
      {slides.map((slide)=> (
      <div className="w-screen snap-center shrink-0 h-full flex flex-col justify-center items-center p-8" key={slide.id}>
        <h1 className="text-center text-4xl font-black">{slide.title}</h1>
        <img className="w-60 h-60 object-contain" src={slide.imgSrc}/>
      </div>
      ))}
    </div>
    <div className="w-full flex flex-col gap-4 justify-center items-center p-8">
   <div className="flex gap-2">
          {slides.map((_, index) => (
            <div 
              key={index}
              className={`h-2 rounded-full transition-all duration-300 ${
                currentSlide === index ? "w-8 bg-teal-400" : "w-2 bg-gray-300"
              }`}
            />
          ))}
        </div>
      <button
      onClick={() => {
            if (currentSlide < slides.length - 1) {
              scrollRef.current?.scrollTo({ left: window.innerWidth * (currentSlide + 1) });
            } else {
              console.log("Ir al Dashboard");
            }
          }}
      className="w-full h-15 font-black flex justify-center items-center bg-teal-400 rounded-2xl">
        Siguiente
      </button>
    </div>
  </div>
}