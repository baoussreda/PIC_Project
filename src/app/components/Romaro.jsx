"use client";
import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import axios from 'axios';
import GithubIcon from "../../../public/github-icon.svg";
import LinkedinIcon from "../../../public/linkedin-icon.svg";

//hosting my backend codebase later on a cloud FaaS

const PythonServerUrl = "http://127.0.0.1:5000"; 


const Romaro = () => {
  const [file, setFile] = useState(null);
  const [antennaResponse, setAntennaResponse] = useState(null);


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleGetAutoLISP = async () => {
    try {
      if (file) {
        const formData = new FormData();
        formData.append("image", file);
  
        const response = await axios.post(`${PythonServerUrl}/download-script`, formData, {
          responseType: 'blob',
        });
  
        if (!response.status === 200) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
  
        const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
  
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = 'generated_files.zip';
  
        document.body.appendChild(link);
  
        link.click();
  
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
      }
    } catch (error) {
      console.error("Error getting AutoLISP script and DWG file:", error);
    }
  };
  
  
  
  const handleGetAntennaType = async (e) => {
    e.preventDefault();
  
    try {
      if (file) {
        const formData = new FormData();
        formData.append("image", file);
  
        const responseTextResponse = await fetch(`${PythonServerUrl}/AntennaType`, {
          method: 'POST',
          body: formData,
        });
  
        if (!responseTextResponse.ok) {
          throw new Error(`HTTP error! Status: ${responseTextResponse.status}`);
        }
  
        const responseText = await responseTextResponse.text();
  
        setAntennaResponse(responseText);
  
        const downloadResponse = await fetch(`${PythonServerUrl}/download-image`, {
          method: 'POST',
          body: formData,
        });
  
        if (!downloadResponse.ok) {
          throw new Error(`HTTP error! Status: ${downloadResponse.status}`);
        }
  
        const blob = await downloadResponse.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        window.open(blobUrl, '_blank');
      }
    } catch (error) {
      console.error("Error getting antenna type:", error);
    }
  };
  

  return (
    <section
      id="Essayer"
      className="grid md:grid-cols-2 my-12 md:my-12 py-24 gap-8 relative bg-gradient-to-br from-primary-900 to-transparent rounded-md p-8 max-w-full"
    >
      <div className="z-10">
        <h5 className="text-3xl font-bold text-white mb-4">
          Let&apos;s Connect
        </h5>
        <p className="text-[#ADB7BE] mb-8 max-w-md">
          I&apos;m currently looking for new opportunities, and my inbox is always open. Whether you have a question or just want to say hi, I&apos;ll do my best to get back to you!
        </p>
        <div className="socials flex flex-row gap-4">
          <Link href="github.com">
            <div className="text-white hover:text-gray-300">
              <Image src={GithubIcon} alt="Github Icon" />
            </div>
          </Link>
          <Link href="linkedin.com">
            <div className="text-white hover:text-gray-300">
              <Image src={LinkedinIcon} alt="Linkedin Icon" />
            </div>
          </Link>
        </div>
      </div>
      <div>
          <form className="flex flex-col space-y-4">
            <div>
              <label htmlFor="file" className="text-white text-lg font-semibold " style={{ marginRight: '10px' }} >
                Choose Image
              </label>
              <input
                name="file"
                type="file"
                id="file"
                accept="image/*"
                required
                onChange={handleFileChange}
                className="text-white p-2 bg-primary-700 border border-[#33353F] rounded-lg w-full"
              />
            </div>
            <div className="flex space-x-4">
            <button
                type="button"
                onClick={handleGetAutoLISP}
                className="bg-primary-500 hover:bg-primary-600 text-white font-medium py-3 rounded-lg flex-grow"               
              >
                Get AutoLISP Script
              </button>

          
              <button
        onClick=
          { handleGetAntennaType
        }
          className="bg-primary-500 hover:bg-primary-600 text-white font-medium py-3 rounded-lg flex-grow"        
              >
                  <div >                    
                    What is the type of this antenna?
                  </div>
                  {antennaResponse && (
        <div>
          <p className="text-green-500 text-lg mb-4">{antennaResponse}</p>
        </div>
      )}
  
                </button>

            </div>
          </form>
      </div>
    </section>
  );
  
};

export default Romaro;
