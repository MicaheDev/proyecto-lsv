
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
  return <div className="w-full h-svh flex flex-col overflow-hidden overflow-x-auto font-google">
    
    <div className="w-[300vw] h-full flex">
      {slides.map((slide)=> (
      <div className="w-[100vw] h-full flex flex-col justify-center items-center border" key={slide.id}>
        {slide.title}
        
        <img src={slide.imgSrc}/>
      </div>
      ))}
    </div>
  </div>
}