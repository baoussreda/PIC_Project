"use client";
import React, { useState, useRef } from "react";
import ProjectCard from "./ProjectCard";
import ProjectTag from "./ProjectTag";
import { motion, useInView } from "framer-motion";

const projectsData = [
  {
    id: 1,
    title: "Circet Italia reprend Tekna Servizi S.r.l.",
    description: "",
    image: "/images/projects/1.png",
    tag: ["All", "Circet France"],
    gitUrl: "/",
    previewUrl: "/",
  },
  {
    id: 2,
    title: "MAM-Bau rejoint Circet Deutschland",
    description: "",
    image: "/images/projects/2.png",  
    tag: ["All", "Circet France"],
    gitUrl: "/",
    previewUrl: "/",
  },
  {
    id: 3,
    title: "Circet Benelux acquiert Gritt Projects",
    description: "",
    image: "/images/projects/3.png",
    tag: ["All", "Circet France"],
    gitUrl: "/",
    previewUrl: "/",
  },
  {
    id: 4,
    title: "Circet ouvre une filiale au Maroc.",
    description: "",
    image: "/images/projects/4.png",
    tag: ["All", "Circet Maroc"],
    gitUrl: "/",
    previewUrl: "/",
  },
  {
    id: 5,
    title: "Leader européen des infrastructures télécoms, Circet souhaite accompagner les opérateurs dans l'ingénierie",
    description: "",
    image: "/images/projects/5.jpg",
    tag: ["All", "Circet Maroc"],
    gitUrl: "/",
    previewUrl: "/",
  },
  {
    id: 6,
    title: "TSA rejoint le groupe Circet",
    description: "",
    image: "/images/projects/6.jpg",
    tag: ["All", "Circet Maroc"],
    gitUrl: "/",
    previewUrl: "/",
  },
];

const ProjectsSection = () => {
  const [tag, setTag] = useState("All");
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  const handleTagChange = (newTag) => {
    setTag(newTag);
  };

  const filteredProjects = projectsData.filter((project) =>
    project.tag.includes(tag)
  );

  const cardVariants = {
    initial: { y: 50, opacity: 0 },
    animate: { y: 0, opacity: 1 },
  };

  return (
    <section id="projects">
      <h2 className="text-center text-4xl font-bold text-white mt-4 mb-8 md:mb-12">
        Nos avancements
      </h2>
      <div className="text-white flex flex-row justify-center items-center gap-2 py-6">
        <ProjectTag
          onClick={handleTagChange}
          name="All"
          isSelected={tag === "All"}
        />
        <ProjectTag
          onClick={handleTagChange}
          name="Circet France"
          isSelected={tag === "Web"}
        />
        <ProjectTag
          onClick={handleTagChange}
          name="Circet Maroc"
          isSelected={tag === "Mobile"}
        />
      </div>
      <ul ref={ref} className="grid md:grid-cols-3 gap-8 md:gap-12">
        {filteredProjects.map((project, index) => (
          <motion.li
            key={index}
            variants={cardVariants}
            initial="initial"
            animate={isInView ? "animate" : "initial"}
            transition={{ duration: 0.3, delay: index * 0.4 }}
          >
            <ProjectCard
              key={project.id}
              title={project.title}
              description={project.description}
              imgUrl={project.image}
              gitUrl={project.gitUrl}
              previewUrl={project.previewUrl}
            />
          </motion.li>
        ))}
      </ul>
    </section>
  );
};

export default ProjectsSection;
