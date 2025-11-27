// import React, { useState } from "react";
// import { DndContext, useDraggable, useDroppable } from "@dnd-kit/core";
// import "./DashBoard.css";
// import WarningCard from "./components/WarningCard.jsx";
// import { VscHome } from "react-icons/vsc";
// import { useNavigate } from "react-router-dom";

// import AppThemeProvider from "./components/graphs/Theme.jsx";
// import BarChart from "./components/graphs/MixedBarChart.jsx";
// import BarGraphHorizontal from "./components/graphs/BarChartHorizontal.jsx";
// import BarAnimation from "./components/graphs/BarAnimation.jsx";

// import { IoIosArrowBack } from "react-icons/io";
// import { IoIosArrowForward } from "react-icons/io";
// import { TbDragDrop } from "react-icons/tb";


// const widgetComponents = {
//   widget1: (
//     <AppThemeProvider mode="dark">
//       <BarChart className="barchart" />
//     </AppThemeProvider>
//   ),
//   widget2: (
//     <AppThemeProvider mode="dark">
//       <BarGraphHorizontal className="reveal"></BarGraphHorizontal>
//     </AppThemeProvider>
//   ),
//   widget3: (
//     <AppThemeProvider mode="dark">
//       <BarAnimation className="reveal"></BarAnimation>
//     </AppThemeProvider>
//   ),
//   widget4:
//   <div><p>ajouter carte</p></div>
// };


// /* ============================
//    DRAGGABLE ITEM
// ============================ */
// function DraggableItem({ id, label }) {
//   const { attributes, listeners, setNodeRef, transform } = useDraggable({ id });

//   const style = transform
//     ? { transform: `translate(${transform.x}px, ${transform.y}px)` }
//     : undefined;

//   return (
//     <div
//       ref={setNodeRef}
//       style={style}
//       {...attributes}
//       {...listeners}
//       className="widget-item"
//     >
//       {label}
//     </div>
//   );
// }

// /* ============================
//    DROPPABLE CONTAINER
// ============================ */

// function DroppableContainer({ id, children }) {
//   const { isOver, setNodeRef } = useDroppable({ id: `drop-${id}` });

//   const isEmpty = React.Children.count(children) === 0;

//   return (
//     <div
//       id={`drop-${id}`}
//       ref={setNodeRef}
//       className={`container ${isOver ? "is-over" : ""}`}
//     >
//       {isEmpty && (
//         <div className="icon-container">
//           <TbDragDrop size={100} />
//         </div>
//       )}

//       {children}
//     </div>
//   );
// }

// /* ============================
//    DASHBOARD
// ============================ */
// export default function Dashboard() {
//   const navigate = useNavigate();
//   const [sidebarOpen, setSidebarOpen] = useState(true);


//   const [containers, setContainers] = useState({
//     c1: [],
//     c2: [],
//     c3: [],
//     c4: [],
//   });

//   const [warningVisible, setWarningVisible] = useState(false);
//   const [pendingDrop, setPendingDrop] = useState(null);

//   const items = [
//     { id: "widget1", label: "Widget 1" },
//     { id: "widget2", label: "Widget 2" },
//     { id: "widget3", label: "Widget 3" },
//     { id: "widget4", label: "Widget 4" },
//   ];

//   /* ============================
//      LOGIQUE DE DROP
//   ============================ */
//   const handleDragEnd = (event) => {
//     const { active, over } = event;
//     if (!over) return;

//     const widgetId = active.id;
//     const containerId = over.id.replace("drop-", ""); // <-- FIX

//     console.log("DROP:", { widgetId, containerId });

//     const current = containers[containerId][0];

//     // if (current === widgetId) return;

//     if (current) {
//       setPendingDrop({ widgetId, containerId });
//       setWarningVisible(true);
//       return;
//     }

//     setContainers((prev) => ({
//       ...prev,
//       [containerId]: [widgetId],
//     }));
//   };

//   /* ============================
//      CONFIRMATION DE REMPLACEMENT
//   ============================ */
//   const confirmReplace = () => {
//     if (!pendingDrop) return;
//     const { widgetId, containerId } = pendingDrop;

//     setContainers((prev) => ({
//       ...prev,
//       [containerId]: [widgetId],
//     }));

//     setWarningVisible(false);
//     setPendingDrop(null);
//   };

//   const cancelReplace = () => {
//     setWarningVisible(false);
//     setPendingDrop(null);
//   };

//   /* ============================
//      RENDER
//   ============================ */

//   return (
//   <>
//     <DndContext onDragEnd={handleDragEnd}>
//       <div className="dashboard-background">

//         {/* Sidebar */}
//         <div className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
//           <button className="home-btn" onClick={() => navigate("/")}>
//             <VscHome size={20} style={{ marginRight: "0px" }} />
//           </button>
//           <h2>Widgets</h2>
//           {items.map((item) => (
//             <DraggableItem key={item.id} id={item.id} label={item.label} />
//           ))}
//         </div>

//         {/* Toggle button EN DEHORS de la sidebar */}
        
//         <button
//           className={`toggle-sidebar-btn ${sidebarOpen ? "open" : "closed"}`}
//           onClick={() => setSidebarOpen(!sidebarOpen)}
//         >
//           {sidebarOpen ? <IoIosArrowBack size={20}/> : <IoIosArrowForward size={20}/>}
//         </button>

//         {/* Bouton Home + grid */}
//         <div className="dashboard-grid">

//           {Object.keys(containers).map((key) => (
//             <DroppableContainer key={key} id={key}>
//               {containers[key].map((itemId) => (
//                 <div key={itemId} className="dropped-widget">
//                   {widgetComponents[itemId] || <div>Widget inconnu</div>}
//                 </div>
//               ))}
//             </DroppableContainer>
//           ))}
//         </div>
//       </div>
//     </DndContext>

//     <WarningCard
//       visible={warningVisible}
//       onConfirm={confirmReplace}
//       onCancel={cancelReplace}
//     />
//   </>
// );

// }


import React, { useState } from "react";
import { DndContext, useDraggable, useDroppable } from "@dnd-kit/core";
import "./DashBoard.css";
import WarningCard from "./components/WarningCard.jsx";
import { VscHome } from "react-icons/vsc";
import { useNavigate } from "react-router-dom";

import AppThemeProvider from "./components/graphs/Theme.jsx";
import BarChart from "./components/graphs/MixedBarChart.jsx";
import BarGraphHorizontal from "./components/graphs/BarChartHorizontal.jsx";
import BarAnimation from "./components/graphs/BarAnimation.jsx";
import DifferentLength from "./components/graphs/DifferentLength.jsx";
import BasicPie from "./components/graphs/BasicPie.jsx";
import Scatter from "./components/graphs/ScatterSelectors.jsx";
import ScatterRegressionLine from "./components/graphs/ScatterRegressionLine.jsx";

import { IoIosArrowBack } from "react-icons/io";
import { IoIosArrowForward } from "react-icons/io";
import { TbDragDrop } from "react-icons/tb";

/* ============================
   WIDGETS + META (taille)
   size: "normal" | "wide" | "long"
   (tu peux changer les tailles ici)
============================ */

const widgetComponents = {
  widget1: (
    <AppThemeProvider mode="dark">
      <BarChart className="barchart" />
    </AppThemeProvider>
  ),
  widget2: (
    <AppThemeProvider mode="dark">
      <BarGraphHorizontal className="reveal" />
    </AppThemeProvider>
  ),
  widget3: (
    <AppThemeProvider mode="dark">
      <BarAnimation className="reveal" />
    </AppThemeProvider>
  ),
  widget4: (
    <AppThemeProvider mode="dark">
      <DifferentLength className="reveal"></DifferentLength>
    </AppThemeProvider>
  ),
  widget5: (
    <AppThemeProvider mode="dark">
      <BasicPie className="reveal"></BasicPie>
    </AppThemeProvider>
  ),
  widget6: (
    <AppThemeProvider mode="dark">
      <Scatter className="reveal"></Scatter>
    </AppThemeProvider>
  ),
  widget7: (
    <AppThemeProvider mode="dark">
      <ScatterRegressionLine className="reveal"></ScatterRegressionLine>
    </AppThemeProvider>
  ),
  widget8: <div><p>ajouter carte</p></div>,
};

const widgetMeta = {
  widget1: { label: "Widget 1", size: "normal" },   // 1x2
  widget2: { label: "Widget 2", size: "long" },   // 2x1
  widget3: { label: "Widget 3", size: "normal" }, // 1x1
  widget4: { label: "Widget 4", size: "wide" }, // 1x1
  widget5: { label: "Widget 5", size: "normal" },
  widget6: { label: "Widget 6", size: "normal" },
  widget7: { label: "Widget 7", size: "normal" },
  widget8: { label: "Widget 8", size: "normal" },
};

/* ============================
   DRAGGABLE ITEM
============================ */
function DraggableItem({ id, label }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    isDragging,       // 🟡 on récupère l'état de drag
  } = useDraggable({ id });

  const style = {
    transform: transform
      ? `translate3d(${transform.x}px, ${transform.y}px, 0)`
      : undefined,
    position: isDragging ? "relative" : "static", // z-index ne marche que si pas "static"
    zIndex: isDragging ? 9999 : "auto",          // 🟣 on force au-dessus de tout
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="widget-item"
    >
      {label}
    </div>
  );
}


/* ============================
   DROPPABLE CONTAINER
============================ */

function DroppableContainer({ id, children, size = "normal" }) {
  const { isOver, setNodeRef } = useDroppable({ id: `drop-${id}` });

  const isEmpty = React.Children.count(children) === 0;

  const sizeClass =
    size === "wide"
      ? "container-wide"
      : size === "long"
      ? "container-long"
      : "";

  return (
    <div
      id={`drop-${id}`}
      ref={setNodeRef}
      className={`container ${isOver ? "is-over" : ""} ${sizeClass}`}
    >
      {isEmpty && (
        <div className="icon-container">
          <TbDragDrop size={100} />
        </div>
      )}

      {children}
    </div>
  );
}

/* ============================
   DASHBOARD
============================ */
export default function Dashboard() {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Contenu des containers (quel widget est dedans)
  const [containers, setContainers] = useState({
    c1: [],
    c2: [],
    c3: [],
    c4: [],
    c5: [],
    c6: [],
  });

  // Taille des containers (normal | wide | long)
  const [containerSizes, setContainerSizes] = useState({
    c1: "normal",
    c2: "normal",
    c3: "normal",
    c4: "normal",
    c5: "normal",
    c6: "normal",
  });

  const [warningVisible, setWarningVisible] = useState(false);
  const [pendingDrop, setPendingDrop] = useState(null);

  const items = Object.entries(widgetMeta).map(([id, cfg]) => ({
    id,
    label: cfg.label,
  }));

  /* ============================
     LOGIQUE DE DROP
  ============================ */
  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (!over) return;

    const widgetId = active.id;
    const containerId = over.id.replace("drop-", "");

    console.log("DROP:", { widgetId, containerId });

    const current = containers[containerId][0];
    const widgetSize = widgetMeta[widgetId]?.size || "normal";

    if (current) {
      // On demande confirmation pour remplacer
      setPendingDrop({ widgetId, containerId, size: widgetSize });
      setWarningVisible(true);
      return;
    }

    // Pas de widget dans ce container : on set directement
    setContainers((prev) => ({
      ...prev,
      [containerId]: [widgetId],
    }));

    setContainerSizes((prev) => ({
      ...prev,
      [containerId]: widgetSize,
    }));
  };

  /* ============================
     CONFIRMATION DE REMPLACEMENT
  ============================ */
  const confirmReplace = () => {
    if (!pendingDrop) return;
    const { widgetId, containerId, size } = pendingDrop;

    setContainers((prev) => ({
      ...prev,
      [containerId]: [widgetId],
    }));

    setContainerSizes((prev) => ({
      ...prev,
      [containerId]: size,
    }));

    setWarningVisible(false);
    setPendingDrop(null);
  };

  const cancelReplace = () => {
    setWarningVisible(false);
    setPendingDrop(null);
  };

  /* ============================
     RENDER
  ============================ */

  return (
    <>
      <DndContext onDragEnd={handleDragEnd}>
        <div className="dashboard-background">
          {/* Sidebar */}
          <div className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
            <button className="home-btn" onClick={() => navigate("/")}>
              <VscHome size={20} style={{ marginRight: "0px" }} />
            </button>
            <h2>Widgets</h2>
            {items.map((item) => (
              <DraggableItem key={item.id} id={item.id} label={item.label} />
            ))}
          </div>

          {/* Bouton toggle de la sidebar */}
          <button
            className={`toggle-sidebar-btn ${sidebarOpen ? "open" : "closed"}`}
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <IoIosArrowBack size={20} /> : <IoIosArrowForward size={20} />}
          </button>

          {/* Grid principale */}
          <div className="dashboard-grid">
            {Object.keys(containers).map((key) => (
              <DroppableContainer
                key={key}
                id={key}
                size={containerSizes[key]}
              >
                {containers[key].map((itemId) => (
                  <div key={itemId} className="dropped-widget">
                    <div className="chart-wrapper">
                      {widgetComponents[itemId] || <div>Widget inconnu</div>}
                    </div>
                  </div>
                ))}
              </DroppableContainer>
            ))}
          </div>
        </div>
      </DndContext>

      <WarningCard
        visible={warningVisible}
        onConfirm={confirmReplace}
        onCancel={cancelReplace}
      />
    </>
  );
}
