import BottomBar from "../components/BottomBar";
import Scaffold from "../components/Scaffold";
import TopBar from "../components/TopBar";

type Props = {};

export default function Learn({}: Props) {
  return <Scaffold TopBar={<TopBar />} BottomBar={<BottomBar />}>

    <h1>hola</h1>
  </Scaffold>;
}
