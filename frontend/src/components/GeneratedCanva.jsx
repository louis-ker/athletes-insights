export default function GeneratedCanva({ data }) {
  if (!data) return null;

  // 🔧 récupérer la question initiale (backend > fallback front)
  const initialQuestion =
    data.original_question ||
    data._originalQuestion ||                 // fallback ajouté côté MessageBox
    data?.header?.question ||
    data?.header?.content ||
    "";

  return (
    <div style={{ padding: "1rem" }}>
      {/* Question initiale */}
      <h4 style={{ marginTop: 0 }}>Initial Question</h4>
      <p>{initialQuestion}</p>

      {/* Titre principal */}
      <h2 style={{ marginTop: "1rem" }}>
        {data?.header?.content || "Titre"}
      </h2>

      {/* Parts en ordre fixe */}
      {["part1", "part2", "part3"].map((key) => {
        const part = data?.[key];
        if (!part) return null;
        return (
          // <section key={key} style={{ marginTop: "1rem" }}>
          <div>
            <h3>{part.title}</h3>
            <p>{part.generated_answer || "—"}</p>
          </div>
          // </section>
        );
      })}
    </div>
  );
}
