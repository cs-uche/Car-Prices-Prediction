# Data Versioning

Version control, a well-established practice in software development, extends its significance to production machine learning. While the conventional understanding of version control predominantly revolves around source code, in machine learning it extends to data.

Data versioning is a pivotal element that often plays a decisive role in the reproducibility and reliability of models. Every iteration of a model is not only shaped by the algorithms and code but is equally influenced by the datasets it learns from. Changes in the underlying data can significantly impact model performance, and having a systematic approach to manage these alterations becomes indispensable.

## The Challenge of Scale and Collaboration
As our models grow in complexity and datasets expand, the traditional practice of saving data locally reveals its limitations. What worked seamlessly for smaller datasets becomes a bottleneck in collaborative scenarios. The need for scalability and the ability to seamlessly collaborate becomes paramount.

## The Power of the Cloud 

In our exploration, we unravel a strategic recommendation that transforms the way we handle data versions — a shift from local storage to the boundless expanse of the cloud. The accompanying notebook highlights the steps of saving data locally, shedding light on its practicality for smaller datasets.

Recognizing the limitations of local storage, the notebook concludes with a strategic recommendation: harnessing the power of the cloud for storing data versions. Our recommendation takes center stage, highlighting AWS S3 as the cloud's data warehouse. This cloud-centric strategy capitalizes on the scalability and high availability inherent in cloud-based storage solutions, ensuring seamless data versioning in the expansive landscape of machine learning workflows.


## The Transformation
Witness the transformation as we journey from local data versioning to the cloud. The accompanying visuals paint a compelling picture — a juxtaposition of the familiar local storage landscape against the horizon of cloud-based possibilities.
* Local Data Versioning
<br/>![Local Data Versioning](/imgs/local_data_versioning.png)

* Cloud  Data Versioning
<br/>![Cloud Data Versioning](/imgs/cloud_data_versioning.png)
