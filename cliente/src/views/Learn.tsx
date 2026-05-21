import BottomBar from "../components/BottomBar";
import Scaffold from "../components/Scaffold";
import TopBar from "../components/TopBar";

type Props = {};

export default function Learn({}: Props) {
  return <Scaffold TopBar={<TopBar />} BottomBar={<BottomBar />}>

    <div className="w-full h-full px-8 py-6">
      
      <h1>Contenido curso</h1>
    </div>
  </Scaffold>;
}
