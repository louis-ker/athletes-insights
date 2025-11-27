import { useState, useEffect, useRef } from 'react'

import Dock from './components/Dock'
import { VscHome, VscArchive, VscAccount, VscSettingsGear, VscGraphLine } from 'react-icons/vsc'

import styled from 'styled-components'

import Hyperspeed from './components/Hyperspeed';

import './App.css'
// import "./../index.css";
import speedSkatersImage from './assets/speedSkaters.png'

import Chatbot from "./components/Chatbot";

import BarChart from "./components/graphs/MixedBarChart.jsx";
import BarGraphHorizontal from "./components/graphs/BarChartHorizontal.jsx";
import AppThemeProvider from "./components/graphs/Theme.jsx";
import { ThemeProvider } from '@mui/material/styles';
import MessageBox from "./components/MessageBox.jsx";
import BarAnimation from "./components/graphs/BarAnimation.jsx"
import DifferentLength from './components/graphs/DifferentLength.jsx';
import BasicPie from './components/graphs/BasicPie.jsx';
import Scatter from "./components/graphs/ScatterSelectors.jsx";
import ScatterRegressionLine from './components/graphs/ScatterRegressionLine.jsx';
import ScrollReveal from 'scrollreveal';
import GeneratedCanva from './components/GeneratedCanva.jsx';
import GeneratedGraph from './components/GeneratedGraph.jsx';
import GraphsFromResponse from './components/GraphsFromResponse';
import DownButton from './components/DownButton.jsx';
import Loader from "./components/Loader";
import VerticalReelFeed from "./components/VerticalReelFeed";
import { useNavigate } from "react-router-dom";

import GlobeWithControls from "./components/GlobeWithControls.jsx";

import ArticleResponse from "./components/ArticleResponse";


const Page = styled.div`
  width: 100vw;
  height: 100%;
  min-height: 100%;
  box-sizing: border-box;
  padding-bottom: 96px; /* Laisse de la place pour le Dock */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
`
export const hyperspeedPresets = {
  one: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'turbulentDistortion',
    length: 400,
    roadWidth: 10,
    islandWidth: 2,
    lanesPerRoad: 3,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 2,
    carLightsFade: 0.4,
    totalSideLightSticks: 20,
    lightPairsPerRoadWay: 40,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.12, 0.5],
    lightStickHeight: [1.3, 1.7],
    movingAwaySpeed: [60, 80],
    movingCloserSpeed: [-120, -160],
    carLightsLength: [400 * 0.03, 400 * 0.2],
    carLightsRadius: [0.05, 0.14],
    carWidthPercentage: [0.3, 0.5],
    carShiftX: [-0.8, 0.8],
    carFloorSeparation: [0, 5],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0xd856bf, 0x6750a2, 0xc247ac],
      rightCars: [0x03b3c3, 0x0e5ea5, 0x324555],
      sticks: 0x03b3c3
    }
  },
  two: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'mountainDistortion',
    length: 400,
    roadWidth: 9,
    islandWidth: 2,
    lanesPerRoad: 3,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 2,
    carLightsFade: 0.4,
    totalSideLightSticks: 50,
    lightPairsPerRoadWay: 50,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.12, 0.5],
    lightStickHeight: [1.3, 1.7],

    movingAwaySpeed: [60, 80],
    movingCloserSpeed: [-120, -160],
    carLightsLength: [400 * 0.05, 400 * 0.15],
    carLightsRadius: [0.05, 0.14],
    carWidthPercentage: [0.3, 0.5],
    carShiftX: [-0.2, 0.2],
    carFloorSeparation: [0.05, 1],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0xff102a, 0xeb383e, 0xff102a],
      rightCars: [0xdadafa, 0xbebae3, 0x8f97e4],
      sticks: 0xdadafa
    }
  },
  three: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'xyDistortion',
    length: 400,
    roadWidth: 9,
    islandWidth: 2,
    lanesPerRoad: 3,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 3,
    carLightsFade: 0.4,
    totalSideLightSticks: 50,
    lightPairsPerRoadWay: 30,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.02, 0.05],
    lightStickHeight: [0.3, 0.7],
    movingAwaySpeed: [20, 50],
    movingCloserSpeed: [-150, -230],
    carLightsLength: [400 * 0.05, 400 * 0.2],
    carLightsRadius: [0.03, 0.08],
    carWidthPercentage: [0.1, 0.5],
    carShiftX: [-0.5, 0.5],
    carFloorSeparation: [0, 0.1],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0x7d0d1b, 0xa90519, 0xff102a],
      rightCars: [0xf1eece, 0xe6e2b1, 0xdfd98a],
      sticks: 0xf1eece
    }
  },
  four: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'LongRaceDistortion',
    length: 400,
    roadWidth: 10,
    islandWidth: 5,
    lanesPerRoad: 2,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 2,
    carLightsFade: 0.4,
    totalSideLightSticks: 50,
    lightPairsPerRoadWay: 70,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.12, 0.5],
    lightStickHeight: [1.3, 1.7],
    movingAwaySpeed: [60, 80],
    movingCloserSpeed: [-120, -160],
    carLightsLength: [400 * 0.05, 400 * 0.15],
    carLightsRadius: [0.05, 0.14],
    carWidthPercentage: [0.3, 0.5],
    carShiftX: [-0.2, 0.2],
    carFloorSeparation: [0.05, 1],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0xff5f73, 0xe74d60, 0xff102a],
      rightCars: [0xa4e3e6, 0x80d1d4, 0x53c2c6],
      sticks: 0xa4e3e6
    }
  },
  five: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'turbulentDistortion',
    length: 400,
    roadWidth: 9,
    islandWidth: 2,
    lanesPerRoad: 3,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 2,
    carLightsFade: 0.4,
    totalSideLightSticks: 50,
    lightPairsPerRoadWay: 50,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.12, 0.5],
    lightStickHeight: [1.3, 1.7],
    movingAwaySpeed: [60, 80],
    movingCloserSpeed: [-120, -160],
    carLightsLength: [400 * 0.05, 400 * 0.15],
    carLightsRadius: [0.05, 0.14],
    carWidthPercentage: [0.3, 0.5],
    carShiftX: [-0.2, 0.2],
    carFloorSeparation: [0.05, 1],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0xdc5b20, 0xdca320, 0xdc2020],
      rightCars: [0x334bf7, 0xe5e6ed, 0xbfc6f3],
      sticks: 0xc5e8eb
    }
  },
  six: {
    onSpeedUp: () => {},
    onSlowDown: () => {},
    distortion: 'deepDistortion',
    length: 400,
    roadWidth: 18,
    islandWidth: 2,
    lanesPerRoad: 3,
    fov: 90,
    fovSpeedUp: 150,
    speedUp: 2,
    carLightsFade: 0.4,
    totalSideLightSticks: 50,
    lightPairsPerRoadWay: 50,
    shoulderLinesWidthPercentage: 0.05,
    brokenLinesWidthPercentage: 0.1,
    brokenLinesLengthPercentage: 0.5,
    lightStickWidth: [0.12, 0.5],
    lightStickHeight: [1.3, 1.7],
    movingAwaySpeed: [60, 80],
    movingCloserSpeed: [-120, -160],
    carLightsLength: [400 * 0.05, 400 * 0.15],
    carLightsRadius: [0.05, 0.14],
    carWidthPercentage: [0.3, 0.5],
    carShiftX: [-0.2, 0.2],
    carFloorSeparation: [0.05, 1],
    colors: {
      roadColor: 0x080808,
      islandColor: 0x0a0a0a,
      background: 0x000000,
      shoulderLines: 0x131318,
      brokenLines: 0x131318,
      leftCars: [0xff322f, 0xa33010, 0xa81508],
      rightCars: [0xfdfdf0, 0xf3dea0, 0xe2bb88],
      sticks: 0xfdfdf0
    }
  }
};


// ======================= MAIN =======================
export default function HomePage() {

  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMessage = async () => {
    try {
      const res = await fetch('/api/hello')
      const data = await res.json()
      setMessage(data.message)
    } catch (e) {
      setMessage(`Erreur: ${e.message}`)
    }
  }

  const dockItems = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => navigate("/") },
    { icon: <VscGraphLine size={24} />, label: 'Dashboard', onClick: () => navigate("/dashboard") },
    { icon: <VscArchive size={24} />, label: "Feed", onClick: () => navigate("/feed") },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
  ]

  useEffect(() => {
    ScrollReveal().reveal('.reveal', {
      distance: '40px',
      duration: 1000,
      easing: 'ease-out',
      origin: 'bottom',
      interval: 80, // animation en cascade
      reset: true  // passer à true si tu veux que ça se rejoue à chaque scroll
    });
  }, []);

  console.log("App state:", responseData);
  

  return (
    <Page>
        <img src={speedSkatersImage} alt="Description de l'image" />
        <DownButton></DownButton>
        <Hyperspeed
          effectOptions={{
            onSpeedUp: () => { },
            onSlowDown: () => { },
            // distortion: 'turbulentDistortion',
            length: 700,
            roadWidth: 100,
            islandWidth: 0,
            lanesPerRoad: 1,
            fov: 90,
            fovSpeedUp: 150,
            speedUp: 2,
            carLightsFade: 0.8,
            totalSideLightSticks: 20,
            lightPairsPerRoadWay: 4000,
            shoulderLinesWidthPercentage: 0.01,
            brokenLinesWidthPercentage: 0.1,
            brokenLinesLengthPercentage: 1,
            lightStickWidth: [1, 10],
            lightStickHeight: [1.3, 1.7],
            movingAwaySpeed: [60, 80],
            movingCloserSpeed: [-120, -160],
            carLightsLength: [400 * 0.03, 400 * 0.2],
            carLightsRadius: [0.05, 0.14],
            carWidthPercentage: [0.3, 0.5],
            carShiftX: [0, 1],
            carFloorSeparation: [0, 0],
            colors: {
              // Violet Glace
              // roadColor: 0xFFFFFF,
              // islandColor: 0x0a0a0a,
              // background: 0x000000,
              // shoulderLines: 0xFFFFFF,
              // brokenLines: 0xFFFFFF,
              // leftCars: [0xD856BF, 0x6750A2, 0xC247AC],
              // rightCars: [0x03B3C3, 0x0E5EA5, 0x324555],
              // sticks: 0x03B3C3,

              // Trou noir
              // roadColor: 0xffda8a,
              roadColor: 0xffe3a6,
              islandColor: 0x0a0a0a,
              background: 0x000000,
              shoulderLines: 0xFFFFFF,
              brokenLines: 0xFFFFFF,
              leftCars: [0xFFFFFF, 0xfc9803, 0xfc0303],
              rightCars: [0xFFFFFF, 0xFFFFFF, 0xFFFFFF],
              sticks: 0xb300ff,

              // ISU
              // roadColor: 0xd9f1ff,
              // islandColor: 0x0a0a0a,
              // background: 0x000000,
              // shoulderLines: 0xFFFFFF,
              // brokenLines: 0xFFFFFF,
              // leftCars: [0x001aff, 0x001aff, 0x001aff],
              // rightCars: [0x001aff, 0x001aff, 0x001aff],
              // sticks: 0x03B3C3,
            }
          }}
        />
        {/* <div id="chatbot" class="colorBlock chatBot">
          <MessageBox setResponseData={setResponseData} setIsLoading={setIsLoading} ></MessageBox>
        </div>
        {isLoading && (
          <div id="loader_div" className="flex justify-center py-8">
            <Loader />
          </div>
        )}

        {!isLoading && responseData && (
          <>
            <div className="colorBlock paragraph reveal">
              <GeneratedCanva data={responseData} />
            </div>
            <div className="colorBlock paragraph reveal">
              <GraphsFromResponse responseData={responseData} />
            </div>
          </>
        )} */}


<div id="chatbot" className="colorBlock chatBot">
    <MessageBox
      setResponseData={setResponseData}
      setIsLoading={setIsLoading}
    />
  </div>

  {isLoading && (
    <div id="loader_div" className="flex justify-center py-8">
      <Loader />
    </div>
  )}

  {!isLoading && responseData && (
    <>
      <div className="colorBlock paragraph reveal">
        <ArticleResponse data={responseData} />
      </div>

      <div className="colorBlock paragraph reveal">
        <GraphsFromResponse responseData={responseData} />
      </div>
    </>
  )}




        {/* <div id="separator"></div>
        <div className="colorBlock paragraph reveal">
          <h1>DEMO BELOW</h1>
          <h2>ISU DataHack Challenge</h2>
          <p>An Example of what a generated article might look like</p>
        </div>
        <div className="colorBlock paragraph reveal">
          <p>The International Skating Union (ISU) is the international governing body for competitive ice skating disciplines, including figure skating, synchronized skating, speed skating, and short track speed skating.[8] It was founded in Scheveningen, Netherlands, in July 1892,[2] making it one of the oldest international sport federations. The ISU was formed to establish standardized international rules and regulations for the skating disciplines it governs, and to organize international competitions in these disciplines. It is now based in Switzerland.</p>
        </div>

        <div className="colorBlock paragraph reveal">
          <p>The International Skating Union (ISU)[b] was founded in 1892[10] in the Dutch seaside town of Scheveningen.[9] The meeting was attended by 15 men, as the national association representatives from the Netherlands, Great Britain, Germany/Austria, and two clubs from Stockholm (Sweden) and Budapest (Hungary).[9][11] The ISU was the first international winter sports federation[9] to govern speed skating and figure skating,[12][13] as it laid down the rules for speed skating, shortly followed by figure skating.[9] In 1895, the organization streamlined its mission to deal only with amateur competitors, not professionals, and hosted its first amateur skating championship in February 1896 in St. Petersburg, Russia.[14]</p>
        </div>

        <div className="colorBlock paragraph reveal">
          <p>The United States and Canada formed a competing organization, the International Skating Union of America (ISUA), in 1907.[15][16] Over the next two years, 12 European nations had joined the ISU, while the ISUA had only its original two members.[17] The ISUA folded in 1927.[18]</p>
          <p>European and North American figure skaters rarely competed against each other because of differences in their styles of skating.[19] The ISU had "systematized and arranged" the sport of figure skating,[19] with competitions including "a selection of ten or twelve numbers from the ISU programme, ... five minutes' free skating to music, ... [and] special figures" on one foot.[17] According to figure skating historian James R. Hines, the ISU was formed due to the necessity of establishing a schedule of compulsory figures and to adopt the international style of figure skating used outside of North America and Great Britain.[20] In 1911, Canada joined the ISU, leaving the United States as the only major competitor to not be a member.[19] This changed in 1923, when the United States Figure Skating Association joined the ISU[21] and in 1926, the Japanese sport governing body followed to acquire ISU membership.[22]</p>
        </div> */}

        <div className="globe">
          <GlobeWithControls />
        </div>
        <div className="footer"></div>
      {/* <h1>Frontend Vite ⚡</h1>
      <button onClick={fetchMessage}>Parle moi backend !</button>
      {message && <p>{message}</p>}
      <h1>Chat avec RAGFlow 🤖</h1>
      <Chatbot className="reveal"/> */}
    
      <Dock
        items={dockItems}
        panelHeight={96}
        baseItemSize={80}
        magnification={120}
        distance={200}
      />
    </Page>
  )
}
