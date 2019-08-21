# Response to reviewers

## Reviewer 1

> Patrick O'Leary. Review: "Reproducible Workflow on a Public Cloud for Computational Fluid Dynamics". Authorea. July 26, 2019. DOI: [https://doi.org/10.22541/au.156415458.85375575](https://doi.org/10.22541/au.156415458.85375575)
> (CC-BY)

### Comment 1

* [x] Neither the introduction or the paper highlight the thesis or novel contributions. The reader is left to decide for themselves what aspect they believe are important. This needs to be improved. I found the following list to be reasonable possibilities:

1. Use of cloud computing as an alternative to onsite high-performance computing (HPC).
2. Improvement in public cloud offerings in last 2 to 4 years.
3. A proposed reproducible workflow.
4. The author's experiences.

**Reply**

* The main thesis of the paper is the idea of extending the set of open research objects created and shared for reproducibility (what we call "reproducibility packages"), to the automatic configuration of the computing environment on a cloud service. We explain our contribution in text added at the end of paragraph 3 of the Introduction. We also added a new paragraph at the end of the Introduction to emphasize the point that our paper updates the record with respect to the paper by Freniere and co-authors.
* Because many researchers in "traditional" computational fields (compared to data science) are still highly skeptical of using cloud for their work, we feel it's necessary to provide evidence that it's feasible today to complete CFD studies with cloud computing. Specifically, we need to show that cloud offerings today are practical for parallel computing with GPUs. We added a few sentences to the Abstract and to the last paragraph of the Introduction to emphasize this point.
* Another principal concern of researchers considering cloud resources is the cost. We can't address the issue in this paper in every detail. But we do want to communicate the cost of running the experiments we showcase, and share our ideas about how this concern may be addressed in the future (cost should come down, universities should tackle how to charge indirect costs, and maybe funding agencies could make bulk contracts with providers).

**Changes**

* Improve abstract and introduction to highlight present contributions ([8d998af](https://github.com/barbagroup/cloud-repro/commit/8d998af1c47dbaff37ac713472375bafad45678c)).

---

### Comment 2

* [x] the code snippets breakup the prose with generic, easy to find information such as how to instantiate or run a docker image

**Reply**

* We intend this paper to also serve as a mini-tutorial for researchers wanting to adopt more reproducible practices. (This is mentioned in the beginning of Section 2.) We understand that for this reviewer (an expert in cloud computing, and HPC) these things are obvious. We find among our colleagues and at CFD conferences that containers are still an esoteric technology for most applied computational researchers.

**Changes**

* No changes needed.

---

### Comment 3

* [x] Section One - Defines why reproducibility is essential for science and describes the related work but fails to differentiate their work from past contributions. The reader is left to speculate that it is merely an update to M. Schwab et al., C. Boettiger, C. Freniere et al. works. 

**Reply**

* We are citing all of those works in the Introduction. With the new language introduced addressing comment 1, it should be clear now how we extend the work of the previous authors: we propose capturing the cloud environment programmatically and to share with readers the configuration files; we update the record on the observations made by Freniere et al. to the new cloud services introduced in the last two years.

**Changes**

* Improve abstract and introduction to highlight present contributions ([8d998af](https://github.com/barbagroup/cloud-repro/commit/8d998af1c47dbaff37ac713472375bafad45678c)).

---

### Comment 4

Section Two - Walks the reader through the authors' reproducibility workflow outlined in figure 1.

Notes:

* [x] The delete jobs and pool step is missing in figure 1, but presented (including a listing) in the text.
* [x] Do we need to see the content of listing 1 - 4? Why not add a script to the repository and point to it like the YAML config files in examples/snake2d2k35/config_shipyard? 
* [x] The docker build fails on the COPY ../ssh_config stage. Moreover, do the authors want someone to push their image to the authors' docker hub repository? Besides, the repository in footnote 1 contains a typo which highlights the far more significant issues in reproducibility of well-written error-free publications. This paper is a well-written paper, but errors happen.
* [x] The authors generalize that "same container ... can now run at scale." What about the MPI drivers? Does this effect where it can run and what hardware it can use?

**Reply**

* We added the step "Delete jobs and pool" to the workflow in Fig. 1.
* Do we need the listings? — From the reviewer's point of view, these may seem unnecessary, because the reviewer is already an expert in using containers and cloud resources. But we are aiming our paper for readers who are not experts, may have heard of containers as a new and interesting technology, but have never used them. These readers will see from these listings that adopting containers to make their computations more reproducible is not very complicated or time consuming. We want to include these listings as part of the narrative to encourage more researchers to adopt these tools.
* We updated the Dockerfiles to avoid the error message raised during the COPY instruction. We also fixed the typo in the URL of the GitHub repository.
* We do not expect the readers to build the Docker images locally. Indeed, we store the images on DockerHub, so that they can immediately use them. We provide the command-line instructions we used to build the images (as this is part of the workflow). If the readers want to re-build/modify the image locally, we do not expect them to push it to our DockerHub repository. We modified the last paragraph of sub-section 2.1 to reflect our intentions.
* The Docker images were specifically built (on our local workstation) to be able to run MPI applications on RDMA-capable VMs (such as the NC24r instance with a CentOS-based 7.3 HPC image) using multiple-instance tasks on Azure Batch service. The RDMA network on Azure supports MPI traffic for applications running with Intel MPI 5.x (or a later version). (In other words, to take advantage of RDMA on Linux compute nodes, we must use Intel MPI on the nodes.) We added a sentence  over the end of paragraph 4 of the section "Cost Analysis and User Experience" mentioning the Docker image was specifically crafted to be used with Azure Batch service. Thus, we also removed the sentence "same container ... run at scale."

**Changes**

* Fix typo in URL of footnote ([aac96cb](https://github.com/barbagroup/cloud-repro/commit/aac96cba56e532191e700802e250361068553a02)).
* Change directory of the build context so that Docker build does not fail ([67634d9](https://github.com/barbagroup/cloud-repro/commit/67634d915c3a5357dd363b8b8bdc1924e822a3d9)).
* Add step "Delete pool/jobs" to workflow diagram in Fig. 1 ([d612512](https://github.com/barbagroup/cloud-repro/commit/d61251290afc8e59fda135961d70d2804a5adcf8)).
* Remove sentence "same container ... run at scale" ([758e485](https://github.com/barbagroup/cloud-repro/commit/758e485de260cad01c72bdb38f93059593e4fe1b)).
* Mention Docker images were specifically built to run with Azure Batch service ([c908f53](https://github.com/barbagroup/cloud-repro/commit/c908f53bedb699e1ef0853a56ce4353cc21719de)).
* Change "Anyone" to "The reader interested..." ([a84844f](https://github.com/barbagroup/cloud-repro/commit/a84844fca16d25cdfa90d55c35778e2a20130796)).

---

### Comment 5

* [x] At its' core, this paper is describing the use of cloud computing as an alternative to onsite high-performance computing (HPC). At 'scale' is a loaded term in HPC. This paper examines performance improvements in public cloud offerings and compares small runs in the cloud versus a six-year-old onsite HPC system. However, an MPI performance test up to 8 nodes, a mini-application performance tests up to 8 nodes, and a computational fluid dynamics domain science examination of 2 nodes does not adequately explore scaling.

**Reply**

* The language "at scale" indeed can evoke a "leadership computing" scenario (large DOE machines, etc.), and the reviewer is right to protest its use. We rephrased, because we're in the "long tail" setting here, of researchers running in parallel, but moderate size simulations. The runs are still production size for our application, with mesh sizes in the order of 50 million cells, allowing for three-dimensional fluid dynamics studies in the regimes of interest for our research problem.

**Changes**

* Remove sentence "same container ... run at scale" ([758e485](https://github.com/barbagroup/cloud-repro/commit/758e485de260cad01c72bdb38f93059593e4fe1b)).

---

### Comment 6

Section Three - Provides the results in the form of an MPI benchmark and a Poisson mini-application performance analysis, and analysis associated with a standard set of computational science experiments involving flow around a flying snake.

Notes:

* [x] Both the cloud and the six-year old HPC system use FDR Infiniband. Is Azure superior performance a result of tuning, configuration, or age? The analysis provided by this section is that Azure interconnect is improving. Cloud offerings moving from 10 Gbps Ethernet to FDR Infiniband in the past four years makes this result visible without testing. Did we need the OSU benchmarks for verification?
* [x] For the Poisson mini-application, the results again verify Azure has newer hardware than the authors onsite HPC system. However, what was the cause of the variance? Job/Node placement?
* [x] The detailed description of the flying snake workflow is appreciated.

**Reply**

* Is Azure superior performance a result of tuning, configuration, or age? —We didn't apply any manual tuning: both machines are running the same code, but of course the compiler versions are different, and the hardware is different. We are not emphasizing in this paper that performance is "superior" on Azure: just that it is a viable alternative to on-premises HPC clusters (because many researchers continue to be skeptical of cloud). We noticed that the reviewer twice mentions that we're using a "six-year old HPC system." Even if this is an old machine, it is what we have at our university and it is probably the situation for the majority of university researchers that they don't have much choice in regards to the local machines they run on. We certainly are not attempting to do an "apples to oranges" comparison of performance. The point is to dispel the misconception that cloud is (still) inadequate.
* Do we need the OSU benchmark results? We want to showcase that public cloud offerings have improved in the last few years. Our benchmark results show comparable networking performances between our university-managed HPC cluster and Microsoft Azure. We believe it is important to highlight these results as it is still common wisdom that public clouds are inadequate for computational research using HPC. Moreover, Freniere et al. (2016; Computing in Science & Engineering, 18(5), 68) used the same benchmark to compare their local cluster with AWS EC2 and reported performance degradation in networking. With these results, we are updating the readers of CiSE on the improvements of a public cloud such as Microsoft Azure.
* We do not know the cause of the variance in runtime for the Poisson benchmark. However, the benchmark was executed 5 times within a single job task (and thus, on the same physical node), so the variation is not due to Job/Node placement. We have updated the caption of Fig. 3 (Poisson benchmark), detailing the number of MPI processes and the number of GPU devices used per node.

**Changes**

* Add information about the number of MPI processes and the number of GPU devices used per node for the Poisson benchmark ([98fccec](https://github.com/barbagroup/cloud-repro/commit/98fccec0a5a0ba7c6d9b4859a20aa81866417f92)).

---

### Comment 7

Section Four - Explores the cost analysis for a typical set of computational science experiments and insights on the user experience.

Notes:

* [x] For the user experience, how much did free computing and augmented support from Microsoft influence the authors' determination to utilize this environment. If it cost 20K, would the authors have completed the project?
* [x] Pricing changes every month, every week, maybe every day. Will any of this analysis be relevant by publication?
* [x] Table 5 will be outdated by the time this article is published. It does not add value.
* [x] How does this cost compare to buying a 2 - 8 node equivalent cluster? 
* [x] Singularity containers appear out of the blue in this section with no description.
* [x] The reference for Table 5 in the text is just (5). Is this a cite, a figure, or a listing.

**Reply**

* We would not have attempted this work, were it not for the sponsored cloud credits. We were indeed curious about reproducibility benefits of cloud computing, and that's why we wrote the proposal to Azure Research. But without the sponsorship, we would not have had research budget for this work. In our opinion, this is one of the reasons to publish this paper: other researchers curious about using cloud need this kind of information before they will jump in. With regards to support, we used the standard channels (support tickets and GitHub issues), and it was not "augmented" support. We edited the acknowledgement section, which vaguely used the verb "help," to avoid the impression that we received extra support.
* Price will of course change. We feel it needs to go down. The relevancy of publishing the "snapshot" of today's pricing is precisely as back up that prices should drop. However, the cost of the NC24r instance we used in this study has been 3.96 USD per compute hour for the last two years and it's unlikely that it will change by a lot in the next 6 months.
* Table 5 will be outdated, yes, but it is today's situation, under which we operated. It's also the case that the patterns will continue (i.e., the ratio between the different pricing options).
* Cost compared to buying a cluster? We don't really know. We tried to get some helpful data from our IT department, but were denied the information.
* We added a short description about the Singularity container technology at the end of paragraph 3 of the section "Cost Analysis and User Experience."
* We fixed the reference to Table 5 in the manuscript.

**Changes**

* Properly reference Table 5 of the manuscript ([db21f03](https://github.com/barbagroup/cloud-repro/commit/db21f036e8ae47bb4b6ab61d555a28637542ad1a)).
* Add description about Singularity container technology ([df1e0d5](https://github.com/barbagroup/cloud-repro/commit/df1e0d5f009038b2057a3de8a914662972d80769)).
* * Edit acknowledgements ([9772f42](https://github.com/barbagroup/cloud-repro/commit/9772f42a64d01b4aed7ee497a2f41ff88615cf73)).

---

## Reviewer 2

> Witherden, Freddie (2019): Review of Reproducible Workflow on a Public Cloud for Computational Fluid Dynamics. figshare. Online resource. DOI: [https://doi.org/10.6084/m9.figshare.9159740.v1](https://doi.org/10.6084/m9.figshare.9159740.v1)
> (CC-BY)

### Comment 1

* [x] Whilst the manuscript is well written the narrative is somewhat muddled. It starts with an overview of reproducible computational research, then pivots to how containers can be employed within the context of cloud computing, then jumping to benchmarks of one particular cloud providers' hardware, and then -- finally -- pivots a final time to a cost analysis of the public cloud for simulations. These are all interesting topics. Indeed, many a conference proceeding has been dedicated to each of these areas. However, by combining them into a single 10 page document this present manuscript fails to do justice to any of these areas. Further, the high degree of specificity will likely have a negative impact the relevance of the manuscript going forwards; a consequence of it being a review of the current state of affairs of a rapidly evolving field. It would therefore be better if it focused on just one or two areas such as "benchmarking cloud computing platforms" or "reproducibility through containers."

**Reply**

* The main goal of this manuscript is to report how to conduct CFD research in a reproducible way on a public cloud, laying out all the tools we used and the steps we undertook. We intend this paper to also serve as a mini-tutorial for researchers wanting to adopt these reproducible practices (we have observed when giving seminars or domain-conference talks that containers haven't disseminated to the CFD community). We use Docker containers to capture the computational environment and Microsoft Azure tools to capture the run-time environment. The degree of specificity is, in part, the point: precisely reproducing our work presumes deploying the same computational environment.
* Right now, researchers using scientific computing are still concerned about cost and performance on public clouds, and this is why we provide benchmark results and report how much it costs to run our CFD application. Freniere et al. (2016) reported performance degradation on AWS (compared to their local cluster). But in the last three years, cloud providers have improved their offerings for HPC solutions. Thus, another objective is to update the record on the observations made by Freniere et al. (in the same journal) to the new cloud services introduced in the last two years.
* Although cloud computing is a rapidly evolving field, we believe it is important to report on the current state of public cloud offerings for academic applications. 
* The reviewer is a top expert in HPC, and we understand from this point of view it seems the paper does not do justice to the various topics covered. But the intended audience of this paper is not, in fact, either of our reviewers (their expertise was needed, of course, to provide a quality review of the manuscript!). The audience is intended to be researchers using scientific computing (possibly on old and over-subscribed university clusters), who are curious about using cloud resources, and interested in reproducible practices, but need guidelines to adopt these.
* Neither benchmarking cloud computing, nor reproducibility with containers, were a central focus for our paper. We include some benchmark results to update the record with respect to the article by Freniere et al., appearing in the same journal. We use container technology for our reproducible workflow (as others have), but extend the reproducibility ideas to automatic configuration of cloud resources.

**Changes**

* We made several changes, responding to both reviewers, which make the aims of the paper more clear. In particular, the Abstract and Introduction prepare the reader better for the rest of the paper.

---

### Comment 2

* [x] The manuscript only appears to be concerned with reproducibility in the 'now' and pays no consideration to 'link rot' and if one will be able to build and run the proposed containers in 5, 10, or even 20 years. (C.f. Old F77 codes which are expected to remain viable long after the heat death of the universe.) This is one of the most serious issues affecting reproducible research today. 
* [x] Further, the manuscript also glosses over several of the issues regarding deploying containerised applications within an HPC context. One of the most important is with regards to MPI libraries and the fact that many HPC/Cloud environments depend on specific MPI library. For example, Cray machines require Cray MPI, IBM POWER 9 machines require Spectrum MPI, and so on. This results in a 'leaky abstraction' for the container must now concern itself with the idiosyncrasies of the hardware which it is running on.

**Reply**

* Obsolescence of digital research objects, including software libraries and computational environments, is an acknowledged source of non-reproducibility, in the long run. The recent report of the National Academies highlights it so (page 57). Indeed, tools in our workflow that we have no control over (Azure CLI, Batch Shipyard) will likely change, and perhaps not be backwards compatible. That is inevitable. But when they do, our fully documented workflow (via human-readable configuration files) will continue to offer transparency of what we did and how we did it. 
* "issues regarding deploying containerised applications within an HPC context" — Broad portability of our software and workflow is not our objective, and would (arguably) not be justified. Our software is currently only used in research projects within our lab: what reasons would call for the highly skilled and labor intensive software engineering required to deliver broadly portable software and workflow?The goal is, rather, to publish our computational research with deep transparency. The Docker images built for this study were specifically crafted to run on Microsoft Azure with Azure Batch service on RDMA-capable nodes with Linux-based virtual machines. Readers interested in reproducing our analysis should do it under the same conditions, which include the same cloud environment. We have added text in the introduction explaining the limitations of this work with respect to portability issues.

**Changes**

* Added language about limitations regarding portability issues ([97e0512](https://github.com/barbagroup/cloud-repro/commit/97e05126928bea4285c586bfd1f8edc50c0f10ad)).
* Re-arrange last paragraph of the conclusion to emphasize the limitation of the reproducibility, and add citation to the new NASEM report ([6f029e9](https://github.com/barbagroup/cloud-repro/commit/6f029e99103e38b1e4487b08f580a9c1904ba419)).

---

### Comment 3

As highlighted by the authors' in both the manuscript and the Dockerfiles it is necessary (on the Azure platform at least) to use the Intel MPI library. This is highly problematic.

* [x] \(a) It explicitly ties the container to x86 based clusters which support the Intel MPI library (even when the underlying solver software and libraries are portable).
* [x] \(b) The library itself has to be downloaded off a random URL on the Intel website (whose long term stability and availability is suspect).
* [x] \(c) Downloading the library requires acceptance of a proprietary EULA whose terms could easily put an unsuspecting researcher who does not also possess a JD into serious legal trouble with the Intel Corporation -- especially when it comes to moving the container between systems which may be employed for commercial gain. (Aside: whilst in all of the Dockerfiles an rm -rf is performed at the end to remove the Intel components, due to the layered nature of Docker images the compilers are *100%* still present in the resulting images and thus may result in even more legal issues for an unsuspecting researcher.)
* [x] \(d) It is also sub-optimal in the context of CUDA applications for the Intel MPI library is not (to the reviewers' knowledge) CUDA aware and thus parallel CUDA applications are likely to run substantially slower than on say OpenMPI or MVAPICH2 w/GDR.

The result is a highly fragile system which is coupled to the wonts of one particular cloud platform.

Similarly, with the CUDA containers there are also compatibility issues.  The most obvious is the container specifying a specific GPU architecture version which may not map onto the hardware of the host.  This is another 'leaky abstraction' issue.

**Reply**

* (a) As indicated in our reply to Comment 2, portability to other hardware is not our goal. We do, in fact, tie the reproducibility of our results to using the exact same computational environment.
* (b) We downloaded the MPI library from the Intel website just to build the Docker images locally. These images are now published on DockerHub and publicly available. Readers interested in reproducing our analysis under the same conditions (on Azure) do not need to dowload the Intel MPI library.
* (c) The Intel MPI library is under [Intel Simplified Software License](https://software.intel.com/en-us/license/intel-simplified-software-license), which allows for redistribution as long as the copyright note remains. On downloading the library, the LICENSE file is included with the source. There is no mention of commercial uses in the license, so they are not disallowed. Note that we are not using Intel compilers, just the MPI library. For greater transparency, we added a note in the README under the `docker` sub-folder saying the user who downloads the Docker image agrees to the Intel license terms. The same note was also added to the description of the Docker images on DockerHub.
* (d) We _need_ to use Intel MPI library, because the Azure nodes we are using require it. Our software is, indeed, using GPU computing with CUDA. Other MPI libraries may be more performant with CUDA,  but they are not available in the RDMA-capable Azure nodes used. Note that performance is not our highest priority, reproducibility is.

**Changes**

* Add note about Intel Simplified Software License ([d3c8543](https://github.com/barbagroup/cloud-repro/commit/d3c8543be25ff6b2d55947b6a3a118618878d7e3)).

---

### Comment 4

* [x] Table 1 contains performance data for the Azure cloud nodes and the Colonial One nodes. However, it makes no mention of the memory configuration of the nodes (# of channels and speed rating of the DDR memory). Different configurations here can result in substantial differences with regards to peak memory bandwidth. This is vital as all of the benchmarks fall into the category of 'memory bandwidth bound problems'. Along these lines it is also important to note if ECC was enabled or disabled for the NVIDIA GPUs as this can have a substantial impact on performance.

**Reply**

* We agree with the comments made by the reviewer. The memory configuration on Colonial One is 128GB of 1600MHz DDR3 ECC Register DRAM for `ivygpu` nodes and 128GB of 1866MHz DDR3 ECC Registered DRAM for `short` nodes. However, we do not have such information for Azure. We contacted Microsoft Azure about that and they told us there is no publicly released information regarding the speed and channels. Right now, only CPU information are publicly available (already included in Table 1 of the manuscript).
* All runs using GPU computing that are reported in the manuscript were done with ECC enabled for NVIDIA GPUs (on Azure and on Colonial One). As suggested by the reviewer, we added that information to the manuscript (in the caption of Table 1).

**Changes**

* Mention ECC was enabled for GPU computing in caption of Table 1 ([5ad8d81](https://github.com/barbagroup/cloud-repro/commit/5ad8d8100d59b60568cf067be82f6a63546179ea)).

---

### Comment 5

* [x] With regards to the benchmarks in Fig 2. could the authors explain why the lower latency for the Colonial One cluster at small message sizes does not translate into greater peak bandwidth at these sizes?

**Reply**

* We cannot explain that, because we don't know. We did, however, rerun the benchmarks on Colonial One, this time using Intel MPI (previous results used OpenMPI), and the results do get closer to those on Azure. In any case, the age of the system, the details of the hardware, or system software—we don't worry about the details, because the purpose of this figure is to update the reader on similar reports presented 3 years ago by Freniere et al.

**Changes**

* Update Figures 2 and 3 after re-running the benchmarks (MPI and Poisson) on Colonial One with the Intel MPI library; OpenMPI was used in the previous version of the manuscript ([38dd7d0](https://github.com/barbagroup/cloud-repro/commit/38dd7d074dc7bfa109d1c74b59f991d914fe204a)).

---

### Comment 6

* [x] Fig 3 is somewhat cluttered and amounts to three plots in one. The first appears to be strong scaling on CPUs whilst the second two correspond to weak scaling on GPUs (although it is not elucidated as such). This breakdown seems somewhat arbitrary.

**Reply**

* We added parenthetical remarks to the text and restructured the caption, emphasizing the type of scaling shown in each plot (strong, weak). We still like the three panels in one figure, rather than breaking it into three figures: they all deal with the Poisson benchmark on the local cluster and the cloud. It seems like a matter of preference on how to present the data, but it is clear what each plot is presenting.

**Changes**

* Mention "strong scaling" for CPUs and "weak scaling" for GPUs to the text ([38dd7d0](https://github.com/barbagroup/cloud-repro/commit/38dd7d074dc7bfa109d1c74b59f991d914fe204a)).
* Restructure the caption text ([a53ae04](https://github.com/barbagroup/cloud-repro/commit/a53ae040e58be7e3a1d6e2289ba84b97ae889133)).

---

### Comment 7

* [x] On line 45 of page 6 a remark is made around "One of the requirements for reproducible computational results is to make code available under a public license (allowing reuse and modification by others)." However this does not appear to follow; a piece of work whose code and data is made available for "reproducibility purposes only" would still appear to meet the requirements for facilitating reproducible computational results laid out in the introduction even though the license does not permit reuse or modification.

**Reply**

* Strictly speaking, the reviewer is correct. One _could_ make code available under a restrictive license that allows others to _only_ use it without modification to reproduce the results. That is certainly possible, but not good form, in our opinion. We added the word "ideally" in the parenthetical note, to be strictly accurate.

**Changes**

* Add word "ideally" in the parenthetical note ([56028ea](https://github.com/barbagroup/cloud-repro/commit/56028ead2f917bd5f30f0d781f8d5b253cfb7b07)).

---

### Comment 8

* [x] With regards to the CFD results there does not appear to be any kind of mesh/convergence study nor are any attempts made to quantify the uncertainties on the resulting C\_L and C\_D coefficients. As such it is difficult to know what to make of the results beyond "they look nice." Although the reviewer appreciates the focus of this paper is not the CFD results per-se it is nevertheless important when presenting numerical results to make a case that the method is resolving all relevant dynamics and that any time-averaged statistics are indeed converged.

**Reply**

* We do have results of a simulation with a mesh of doubled density in the near-body region, with the same stretching ratio moving away from it. It results in more than 230 million cells. The relative difference in time-averaged force coefficients was 6.5% for drag and 3% for lift. But the cost is about 7.4 times compared with the coarser-grid run shown in the paper. The purpose of this paper is not targeting the physics, but the reviewer is right to ask about the fidelity of the simulation shown, and other readers may have the same question. Therefore, we have added a passage at the end of section 3.3.2 with this very explanation, and added to the GitHub repository for this paper a Jupyter notebook with a comparison of the time-varying force coefficients between the coarser and finer meshes. The paper points to this notebook as supplementary material.

**Changes**

* Add a Jupyter Notebook with comparison of the force coefficients between the coarse and fine grids ([c1ed36e](https://github.com/barbagroup/cloud-repro/commit/c1ed36e143c226b3381898318d2ec0ab70e2994e)).
* Add sentences about the run on the finer grid ([201ef06](https://github.com/barbagroup/cloud-repro/commit/201ef066bd04a76cb715028f805d21da2f86e29b)).

---

### Comment 9

* [x] Although the cost analysis is interesting without any real basis of comparison it is difficult to glean much from it.

**Reply**

* We used the the cloud platform Microsoft Azure because we received a sponsorship from the program "Microsoft Azure for Research." We have not tried other cloud providers. We do not report any cost analysis for local HPC cluster as the University is not willing to disclose information related to the cost of operating the cluster.

**Changes**

* No changes needed.
