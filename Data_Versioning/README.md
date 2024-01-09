# Data Versioning

Version control, a well-established practice in software development, extends its significance to production machine learning. While the conventional understanding of version control predominantly revolves around source code, in machine learning it extends to data versioning.
 
In machine learning, data versioning is a pivotal element that often plays a decisive role in the reproducibility and reliability of models. Every iteration of a model is not only shaped by the algorithms and code but is equally influenced by the datasets it learns from. Changes in the underlying data can significantly impact model performance, and having a systematic approach to manage these alterations becomes indispensable.

This project delves into some methods of data versioning.The accompanying notebook highlights steps for saving the data locally, a practice that, while suitable for smaller datasets, poses challenges in collaborative scenarios and scalability. Recognizing these limitations, the notebook concludes with a strategic recommendation: harnessing the power of the cloud for storing data versions. 

One of the recommentations at the end of the notebook is to leverage the cloud to store the data versions, specifically utilizing AWS S3 as a data warehouse.  This cloud-centric strategy capitalizes on the scalability and high availability inherent in cloud-based storage solutions, ensuring seamless data versioning in the expansive landscape of machine learning workflows.